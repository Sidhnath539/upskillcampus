import json
import os
import random
from datetime import datetime

class QuizGame:
    def __init__(self):
        self.questions_file = "questions.json"
        self.scores_file = "scores.txt"
        self.questions = []
        self.score = 0
        self.current_question = 0
        
    def load_questions(self):
        """Load questions from JSON file"""
        try:
            if os.path.exists(self.questions_file):
                with open(self.questions_file, 'r', encoding='utf-8') as f:
                    self.questions = json.load(f)
                print(f" Loaded {len(self.questions)} questions!")
            else:
                print("❌ Questions file not found. Creating default questions...")
                self.create_default_questions()
                self.load_questions()
        except json.JSONDecodeError:
            print("❌ Error reading questions file. Creating default questions...")
            self.create_default_questions()
            self.load_questions()
    
    def create_default_questions(self):
        """Create default questions if file doesn't exist"""
        default_questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "answer": 2,
                "category": "Geography"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "answer": 1,
                "category": "Science"
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "answer": 1,
                "category": "Literature"
            },
            {
                "question": "What is 15 × 4?",
                "options": ["45", "60", "75", "90"],
                "answer": 1,
                "category": "Math"
            },
            {
                "question": "Which element has the chemical symbol 'O'?",
                "options": ["Gold", "Oxygen", "Osmium", "Oganesson"],
                "answer": 1,
                "category": "Chemistry"
            }
        ]
        
        with open(self.questions_file, 'w', encoding='utf-8') as f:
            json.dump(default_questions, f, indent=2)
        self.questions = default_questions
    
    def display_welcome(self):
        """Display welcome screen"""
        print("\n" + "="*50)
        print(" WELCOME TO THE ULTIMATE QUIZ GAME! ")
        print("="*50)
        print("Test your knowledge across various categories!")
        print("Answer correctly to increase your score!")
        print("-" * 50 + "\n")
    
    def select_category(self):
        """Let user choose category or random"""
        categories = list(set(q["category"] for q in self.questions))
        print(" Available Categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories)+1}. Random (All categories)")
        
        while True:
            try:
                choice = input("\nSelect category (number): ").strip()
                choice = int(choice)
                if 1 <= choice <= len(categories) + 1:
                    if choice == len(categories) + 1:
                        return self.questions
                    return [q for q in self.questions if q["category"] == categories[choice-1]]
                else:
                    print("❌ Invalid choice! Try again.")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def display_question(self, question_data):
        """Display current question with options"""
        print(f"\n Question {self.current_question + 1}")
        print(f"  Category: {question_data['category']}")
        print("-" * 40)
        print(question_data['question'])
        print("-" * 40)
        
        for i, option in enumerate(question_data['options'], 1):
            print(f"{i}. {option}")
        print("-" * 40)
    
    def get_user_answer(self):
        """Get and validate user answer"""
        while True:
            try:
                answer = input("Your answer (number): ").strip()
                answer = int(answer)
                if 1 <= answer <= 4:
                    return answer - 1  # Convert to 0-indexed
                else:
                    print("❌ Please enter a number between 1-4!")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def check_answer(self, user_answer, correct_answer):
        """Check if answer is correct and update score"""
        if user_answer == correct_answer:
            self.score += 10
            print(" Correct! +10 points")
            return True
        else:
            print(f"❌ Wrong! Correct answer was: {correct_answer + 1}")
            return False
    
    def play_game(self):
        """Main game loop"""
        self.load_questions()
        self.display_welcome()
        
        # Select questions
        game_questions = self.select_category()
        random.shuffle(game_questions)
        game_questions = game_questions[:10]  # Limit to 10 questions
        
        self.current_question = 0
        self.score = 0
        
        print(f"\n Starting quiz with {len(game_questions)} questions!\n")
        
        for question_data in game_questions:
            self.display_question(question_data)
            user_answer = self.get_user_answer()
            self.check_answer(user_answer, question_data['answer'])
            self.current_question += 1
            input("\nPress Enter to continue...")
        
        self.show_results()
    
    def show_results(self):
        """Display final results and save high score"""
        percentage = (self.score / 100) * 100
        print("\n" + "="*50)
        print(" QUIZ COMPLETE! ")
        print("="*50)
        print(f" Your Score: {self.score}/100 ({percentage:.1f}%)")
        
        if percentage >= 90:
            print(" PERFECT! You're a genius! ")
        elif percentage >= 80:
            print(" Excellent! Great job! ")
        elif percentage >= 70:
            print(" Very Good! Keep it up! ")
        elif percentage >= 60:
            print(" Good effort! Practice more! ")
        else:
            print(" Keep studying! You'll get better! ")
        
        self.save_high_score()
        print("\n" + "="*50)
    
    def save_high_score(self):
        """Save high score to file"""
        name = input("\nEnter your name for the leaderboard: ").strip() or "Anonymous"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        score_entry = f"{name}|{self.score}|{timestamp}\n"
        
        # Read existing scores
        scores = []
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                scores = f.readlines()
        
        # Add new score
        scores.append(score_entry)
        
        # Sort by score (descending) and keep top 10
        scored_entries = []
        for line in scores:
            parts = line.strip().split('|')
            if len(parts) == 3:
                scored_entries.append((int(parts[1]), line))
        
        scored_entries.sort(reverse=True, key=lambda x: x[0])
        top_scores = [entry[1] for entry in scored_entries[:10]]
        
        # Save back to file
        with open(self.scores_file, 'w') as f:
            f.writelines(top_scores)
        
        self.show_leaderboard()
    
    def show_leaderboard(self):
        """Display top scores"""
        print("\n TOP 10 LEADERBOARD ")
        print("-" * 40)
        
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                scores = f.readlines()
            
            for i, line in enumerate(scores[:10], 1):
                parts = line.strip().split('|')
                if len(parts) == 3:
                    print(f"{i}. {parts[0]:10s} | {parts[1]:3s} pts | {parts[2]}")
        else:
            print("No scores yet!")
    
    def show_menu(self):
        """Main menu"""
        while True:
            print("\n-------------------WELCOME TO QUIZ GAME---------------")
            print("\n MAIN MENU ")
            print("1. Play Quiz")
            print("2. View Leaderboard")
            print("3. Add Custom Question")
            print("4. Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.show_leaderboard()
            elif choice == '3':
                self.add_custom_question()
            elif choice == '4':
                print(" Thanks for playing! See you next time!")
                break
            else:
                print("❌ Invalid option!")
    
    def add_custom_question(self):
        """Add custom question to database"""
        print("\n ADD CUSTOM QUESTION")
        print("-" * 30)
        
        question = input("Enter question: ").strip()
        options = []
        for i in range(4):
            option = input(f"Option {i+1}: ").strip()
            options.append(option)
        
        correct = -1
        while correct < 0 or correct > 3:
            try:
                correct = int(input("Correct answer (1-4): ")) - 1
            except ValueError:
                print("Please enter 1-4!")
        
        category = input("Category (or press Enter for 'General'): ").strip() or "General"
        
        new_question = {
            "question": question,
            "options": options,
            "answer": correct,
            "category": category
        }
        
        # Load existing questions
        self.load_questions()
        self.questions.append(new_question)
        
        # Save updated questions
        with open(self.questions_file, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=2)
        
        print(" Question added successfully!")

def main():
    game = QuizGame()
    game.show_menu()

if __name__ == "__main__":
    main()