import pandas as pd
import pickle

class CourseRecommender:
    def __init__(self, csv_path='Course_Goal_Dataset.csv'):
        # Load course data from CSV file
        self.courses = pd.read_csv(csv_path)
        
        # Ensure column names match expected attributes
        self.courses.rename(columns={
            'Course ID': 'course_id',
            'Course Name': 'course_name',
            'Course Description': 'description',
            'Goal ID': 'goal_id',
            'Goal Name': 'goal'
        }, inplace=True)
        
    def recommend_courses(self, goal):
        goal = goal.lower()
        
        # Filter courses based on the user's goal
        recommended_courses = self.courses[self.courses['goal'].str.contains(goal, case=False, na=False)]
        
        return recommended_courses.to_dict(orient='records') if not recommended_courses.empty else []

# Create an instance of CourseRecommender
recommender = CourseRecommender()

# Save the recommender model
with open('model.pkl', 'wb') as file:
    pickle.dump(recommender, file)

print("model.pkl has been successfully created.")
