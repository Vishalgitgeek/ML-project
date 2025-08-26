import pandas as pd
import sys
import os
from typing import Tuple, List, Dict
import logging
from io import StringIO

# Add the parent directory to sys.path to import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pipeline.predict_pipeline import PredictPipeline
from src.exception import Custom_Exception
from .models import BatchPrediction, PredictionRecord

logger = logging.getLogger(__name__)

class BatchPredictionService:
    def __init__(self):
        self.prediction_pipeline = PredictPipeline()
        
    def process_csv_file(self, csv_file, filename: str, user=None) -> BatchPrediction:
        """
        Process uploaded CSV file and make batch predictions
        
        Args:
            csv_file: Uploaded CSV file
            filename: Original filename
            user: User object (optional)
            
        Returns:
            BatchPrediction object
        """
        try:
            # Read CSV file
            file_content = csv_file.read().decode('utf-8')
            df = pd.read_csv(StringIO(file_content))
            
            # Create batch prediction record
            batch = BatchPrediction.objects.create(
                user=user,
                filename=filename,
                total_records=len(df),
                status='PROCESSING'
            )
            
            logger.info(f"Started processing batch {batch.id} with {len(df)} records")
            
            # Process each row
            successful_predictions = 0
            failed_predictions = 0
            
            for index, row in df.iterrows():
                try:
                    # Prepare input data for prediction
                    input_data = {
                        'gender': [row['gender']],
                        'race/ethnicity': [row['race/ethnicity']],
                        'parental level of education': [row['parental level of education']],
                        'lunch': [row['lunch']],
                        'test preparation course': [row['test preparation course']],
                        'reading score': [int(row['reading score'])],
                        'writing score': [int(row['writing score'])]
                    }
                    
                    # Make prediction
                    prediction = self.prediction_pipeline.predict(input_data)[0]
                    
                    # Store successful prediction
                    PredictionRecord.objects.create(
                        batch=batch,
                        row_number=index + 1,
                        gender=row['gender'],
                        race_ethnicity=row['race/ethnicity'],
                        parental_level_of_education=row['parental level of education'],
                        lunch=row['lunch'],
                        test_preparation_course=row['test preparation course'],
                        reading_score=int(row['reading score']),
                        writing_score=int(row['writing score']),
                        predicted_math_score=float(prediction),
                        is_successful=True
                    )
                    
                    successful_predictions += 1
                    
                except Exception as e:
                    # Store failed prediction
                    PredictionRecord.objects.create(
                        batch=batch,
                        row_number=index + 1,
                        gender=row.get('gender', ''),
                        race_ethnicity=row.get('race/ethnicity', ''),
                        parental_level_of_education=row.get('parental level of education', ''),
                        lunch=row.get('lunch', ''),
                        test_preparation_course=row.get('test preparation course', ''),
                        reading_score=row.get('reading score', 0) if pd.notna(row.get('reading score')) else 0,
                        writing_score=row.get('writing score', 0) if pd.notna(row.get('writing score')) else 0,
                        is_successful=False,
                        error_message=str(e)
                    )
                    
                    failed_predictions += 1
                    logger.error(f"Failed to process row {index + 1}: {str(e)}")
            
            # Update batch status
            batch.processed_records = successful_predictions
            batch.failed_records = failed_predictions
            batch.status = 'COMPLETED' if failed_predictions == 0 else 'COMPLETED'
            batch.save()
            
            logger.info(f"Completed batch {batch.id}: {successful_predictions} successful, {failed_predictions} failed")
            
            return batch
            
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            if 'batch' in locals():
                batch.status = 'FAILED'
                batch.save()
            raise Custom_Exception(e, sys)
    
    def generate_results_csv(self, batch: BatchPrediction) -> str:
        """
        Generate CSV string with prediction results
        
        Args:
            batch: BatchPrediction object
            
        Returns:
            CSV string with results
        """
        try:
            predictions = batch.predictions.all().order_by('row_number')
            
            data = []
            for pred in predictions:
                data.append({
                    'row_number': pred.row_number,
                    'gender': pred.gender,
                    'race_ethnicity': pred.race_ethnicity,
                    'parental_level_of_education': pred.parental_level_of_education,
                    'lunch': pred.lunch,
                    'test_preparation_course': pred.test_preparation_course,
                    'reading_score': pred.reading_score,
                    'writing_score': pred.writing_score,
                    'predicted_math_score': pred.predicted_math_score if pred.is_successful else 'ERROR',
                    'status': 'SUCCESS' if pred.is_successful else 'FAILED',
                    'error_message': pred.error_message or ''
                })
            
            df = pd.DataFrame(data)
            return df.to_csv(index=False)
            
        except Exception as e:
            logger.error(f"Error generating results CSV: {str(e)}")
            raise Custom_Exception(e, sys)
    
    def get_batch_summary(self, batch: BatchPrediction) -> Dict:
        """
        Get summary statistics for a batch
        
        Args:
            batch: BatchPrediction object
            
        Returns:
            Dictionary with summary statistics
        """
        try:
            predictions = batch.predictions.filter(is_successful=True)
            
            if predictions.exists():
                scores = [pred.predicted_math_score for pred in predictions]
                summary = {
                    'total_records': batch.total_records,
                    'successful_predictions': batch.processed_records,
                    'failed_predictions': batch.failed_records,
                    'success_rate': (batch.processed_records / batch.total_records) * 100,
                    'average_predicted_score': sum(scores) / len(scores),
                    'min_predicted_score': min(scores),
                    'max_predicted_score': max(scores),
                    'status': batch.status
                }
            else:
                summary = {
                    'total_records': batch.total_records,
                    'successful_predictions': 0,
                    'failed_predictions': batch.total_records,
                    'success_rate': 0,
                    'average_predicted_score': 0,
                    'min_predicted_score': 0,
                    'max_predicted_score': 0,
                    'status': batch.status
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating batch summary: {str(e)}")
            raise Custom_Exception(e, sys)