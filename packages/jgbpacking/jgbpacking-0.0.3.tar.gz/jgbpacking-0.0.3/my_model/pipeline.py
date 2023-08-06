from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import StringIndexer, OneHotEncoder,VectorAssembler, Imputer, StandardScaler, MinMaxScaler
from pyspark.sql import SparkSession
from sklearn.metrics import accuracy_score
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import isnan, when, count, col


from my_model.config.core import config


numeric_cols = config.model_config.numericols

objetivo =  config.model_config.target

labelToIndex = StringIndexer(inputCol= objetivo, outputCol="label")

va1 = [VectorAssembler(inputCols=[f], outputCol=('vec_' + f)) for f in numeric_cols]

ss = [StandardScaler(inputCol='vec_' + f, outputCol='scaled_' + f, withMean=True, withStd=True) for f in numeric_cols ]

assemblerInputs = ['scaled_' + f for f in numeric_cols]

va2 = VectorAssembler(inputCols=assemblerInputs, outputCol="features")

lr = LogisticRegression(featuresCol="features", labelCol="label", regParam=1.0)

stages = [labelToIndex] + va1 + ss + [va2] + [lr]

calidad_pipe = Pipeline(stages=stages)







