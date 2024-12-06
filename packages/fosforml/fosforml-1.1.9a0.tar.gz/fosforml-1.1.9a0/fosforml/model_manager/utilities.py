from snowflake.ml.dataset import Dataset
from snowflake.ml.model import custom_model
from snowflake.ml.model import model_signature
from fosforml.constants import SnowflakeSupportedMLFlavours
from fosforml.validators import BYOMValidations
import pandas as pd
import snowflake,json
import cloudpickle
import snowflake

class DatasetManager:
    def __init__(self,
                 model_name,
                 version_name,
                 session,
                 connection_params
                ):
        self.model_name = model_name
        self.version_name = version_name
        self.connection_params = connection_params
        self.datasets_obj = self.get_or_create_dataset_object(model_name,version_name,session)
    
    def get_or_create_dataset_object(self,model_name,version_name,session):
        datasets_obj = Dataset(session=session,
                                database=self.connection_params['database'],
                                schema =self.connection_params['schema'],
                                name=f"{model_name}_{version_name}"
                                )
        try:
            datasets_obj.create(session=session,name=f"{model_name}_{version_name}")
        except Exception as e:
            datasets_obj.load(session=session,name=f"{model_name}_{version_name}")
        
        return datasets_obj
    
    def upload_datasets(self,session,datasets: dict):
        try:
            existings_versions = self.datasets_obj.list_versions()
            if len(existings_versions) > 0:
                for version_name in existings_versions:
                    self.datasets_obj.delete_version(version_name=version_name)
            
            datasets = {k:v for k,v in datasets.items() if v is not None}

            for dataset_name, dataset in datasets.items():
                snowpark_dataset = self.get_snowpark_dataset(session,dataset)
                purpose = self.get_dataset_purpose(dataset_name)
                self.datasets_obj.create_version(version=dataset_name,
                                                 input_dataframe=snowpark_dataset,
                                                 comment=json.dumps(
                                                            {
                                                                "purpose": purpose,
                                                                "dataset_type": "Table"
                                                            }
                                                        ))
                
            return True,f"Successfully uploaded {self.model_name} datasets."
        except Exception as e:
            return False,f"model dataset upload failed, error: {str(e)}"
        
    def remove_datasets(self):
        try:
            self.datasets_obj.delete()
            return True,f"Successfully removed {self.model_name} datasets."
        except Exception as e:
            raise Exception(e)
    
    def read_dataset(self,dataset_name,to_pandas=True):
        try:
            if to_pandas:
                return self.datasets_obj.select_version(version=dataset_name).read.to_pandas()
            return self.datasets_obj.select_version(version=dataset_name).read.to_snowpark_dataframe()
        except Exception as e:
            raise Exception(f"Failed to get dataset {dataset_name}. {str(e)}")
    
    def list_datasets(self):
        try:
            return self.datasets_obj.list_versions()
        except Exception as e:
            raise Exception(f"Failed to list datasets. {str(e)}")
    
    @staticmethod
    def get_dataset_purpose(dataset_name):
        if "x_train" in dataset_name.lower():
            return "Training"
        elif "y_train" in dataset_name.lower():
            return "Training"
        elif "x_test" in dataset_name.lower():
            return "Inference"
        elif "y_test" in dataset_name.lower():
            return "Inference"
        elif "y_pred" in dataset_name.lower():
            return "Validation"
        elif "prob" in dataset_name.lower():
            return "Validation"
        else:
            return "Training"        
        
    def get_snowpark_dataset(self,session,dataset):
        if isinstance(dataset,snowflake.snowpark.dataframe.DataFrame):
            return dataset
        elif isinstance(dataset,pd.DataFrame):
            return session.create_dataframe(dataset)
        
        elif isinstance(dataset,pd.Series):
            return session.create_dataframe(dataset.to_frame())
        else:
            raise Exception("Invalid dataset type to save .")  

class Metadata:
    def __init__(self, model_registry):
        self.model_registry = model_registry

    def update_model_registry(self,
                              model_name,
                              model_description,
                              model_tags,
                              session
                              ):
        try:
            model = self.model_registry.get_model(model_name=model_name)
            model.description = model_description
            self.set_model_tags(session,
                                model,
                                model_name,
                                tags=model_tags)
            
            return f"Updated model metadata for {model_name}."
        except Exception as e:
            print(f"error:{str(e)}")
            return False

    def set_model_tags(self,
                       session,
                       model,
                       model_name,
                       tags={}):
        try:
            for tag_name,tag_value in tags.items():
                session.sql(f"create tag if not exists {tag_name}").collect()
                model.set_tag(
                            tag_name = tag_name,
                            tag_value = tag_value
                            )
        except Exception as e:
            print(f"Failed to set tags for model {model_name}.")
            print(e)
            # pass
            # raise Exception(f"Failed to set tags for model {model_name}")
        

class BYOMRegisrty:
    def __init__(self,
                 model_file,
                 score_func,
                 model_type,
                 model_flavour,
                 sample_input_data,
                 conda_packages,
                ):
        self.model_file = model_file
        self.score = score_func
        self.flag = bool(score_func)
        self.model_type = model_type
        self.model_flavour = model_flavour
        self.sample_data = sample_input_data
        self.conda_packages = conda_packages
        self.mc = custom_model.ModelContext(
        	artifacts={ 
                'model_file': self.model_file
        	}
        )
    

    def byom_model_flow(self):
        if self.model_type.lower() == "forecasting":
            return "forecasting_custom_model"
        elif self.score or self.model_flavour.lower() not in SnowflakeSupportedMLFlavours.list():
            return "non_forecasting_custom_model"
        else:
            return "supported_flavour_without_score"
        
    def forecasting_custom_model(self):
        return self._create_custom_model(forecasting=True)

    def non_forecasting_custom_model(self):
        return self._create_custom_model(forecasting=False)

    def supported_flavour_without_score(self):
        return BYOMValidations.load_validate_model(self.model_file, self.model_flavour, self.conda_packages)

    def get_model_signature(self, c_model):
        df = self.sample_data
        if self.model_type.lower() == "forecasting":
            df['PERIODS'] = 1
        _pred = c_model.predict(df)
        _pred_signature = model_signature.infer_signature(input_data=df, output_data=_pred)
        print(_pred_signature)
        return _pred_signature

    def get_byom_model(self):
        flow = self.byom_model_flow()
        if flow == "forecasting_custom_model":
            return self.forecasting_custom_model()
        elif flow == "non_forecasting_custom_model":
            return self.non_forecasting_custom_model()
        elif flow == "supported_flavour_without_score":
            return self.supported_flavour_without_score()
        else:
            raise ValueError(f"Unknown flow: {flow}")

    def _create_custom_model(self, forecasting):
        score_func = self.score

        class CustomTestModel(custom_model.CustomModel):
            def __init__(self, context: custom_model.ModelContext,forecasting=forecasting,flag=None) -> None:
                super().__init__(context)
                self.forecasting = forecasting
                self.flag = flag
                model_dir = self.context.path("model_file")
                with open(model_dir, 'rb') as file:
                    self.model = cloudpickle.load(file)

            @custom_model.inference_api
            def predict(self, input_data: pd.DataFrame) -> pd.DataFrame:
                model = self.model
                _input_records = input_data.shape[0]
                if self.forecasting:
                    step, _data = self._extract_periods_from_df(input_data)
                    if self.flag:
                        return self._maintain_output_sync(score_func(_data, model, step), _input_records)
                    else:
                        res = model.predict(step)
                        res = res.to_frame()[0].apply(pd.Series)
                        res.columns = ['PREDICTIONS']
                        return self._maintain_output_sync(res, _input_records)
                else:
                    if self.flag:
                        return self._maintain_output_sync(score_func(input_data), _input_records)
                    else:
                        res = model.predict(input_data)
                        return self._maintain_output_sync(res if isinstance(res, pd.DataFrame) else res.to_frame(), _input_records)

            def _extract_periods_from_df(self, data):
                columns = data.columns.tolist()
                values = data.iloc[0].tolist()
                step = 1
                for column, value in zip(columns, values):
                    if column == 'PERIODS':
                        step = int(value)
                        _data = data.drop('PERIODS', axis=1)
                return step, _data
            
            def _maintain_output_sync(self, data, count):
                _add_records = count - data.shape[0]
                _add_df = pd.DataFrame(index=range(_add_records), columns=data.columns)
                data = pd.concat([data, _add_df], ignore_index=True)
                return data

        return CustomTestModel(self.mc, forecasting, self.flag)
    

def log_snowflake_model(
        registry,
        model, 
        model_name, 
        model_version, 
        description, 
        conda_dependencies, 
        metrics, 
        sf_input_dataframe, 
        x_test,
        sample_input_data,
        python_version, 
        score,
        byom_model_sig=None
        ):
    arg_dict = {
        'model': model,
        'model_name': model_name,
        'version_name': model_version,
        'comment': description,
        'conda_dependencies': conda_dependencies,
        'metrics': metrics,
        'python_version': python_version,
    }
    if isinstance(sf_input_dataframe, snowflake.snowpark.dataframe.DataFrame):
        arg_dict['sample_input_data'] = sf_input_dataframe
    elif isinstance(x_test, pd.DataFrame):
        arg_dict['sample_input_data'] = x_test
    if score:
        arg_dict['code_paths'] = [score]
        arg_dict['options'] = {"function_type": "TABLE_FUNCTION"}
    if byom_model_sig: 
        arg_dict['signatures'] = {"predict": byom_model_sig}
    registry.log_model(**arg_dict)