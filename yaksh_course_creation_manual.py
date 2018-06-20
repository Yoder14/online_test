from yaksh.models import *
import os
from django.contrib.auth.models import User
FIXTURES_DIR_PATH = os.path.join(settings.BASE_DIR, 'yaksh', 'fixtures')
user=User.objects.get(email='instructor@mail.com')
course = Course.objects.create(name="Auto Course",enrollment="open",creator=user)
#quizzes are created
questions_list=['question1','question2','question3']
questions_set=['questions1','questions2','questions3']
quizzes=['quiz1','quiz2','quiz3']
que = Question()
learning_module = LearningModule.objects.create(
    name="auto module", description="auto module", creator=user,
    html_data="auto module")
for index,quiz in enumerate(quizzes, 0):
	quiz=Quiz.objects.create(
		start_date_time=timezone.now(),
		end_date_time=timezone.now() + timedelta(176590),
		duration=30, active=True,attempts_allowed=-1,
		time_between_attempts=0,description='Yaksh quiz '+str(index+1),
		pass_criteria=0,creator=user,
		instructions="<b>This is a Quiz 1.</b>")
	print(type(quiz))
	#QUESTIONS
	#questions are uploaded
	# added_questions_lists=[]
	# for question_set in questions_list:
	# questions[question_set]=Question()
	zip_file_path = os.path.join(
		FIXTURES_DIR_PATH, questions_set[index]+'.zip'
		)
	files, extract_path = extract_files(zip_file_path)
	print("files : \n",files)
	print("extract_path : \n",extract_path)
	print("before read yaml")
	print(type(que))
	added_questions = que.read_yaml(extract_path, user, files)
#QUESTION PAPER
# for index, question_paper in enumerate(que_paper_list, 0):
	question_paper = QuestionPaper.objects.create(quiz=quiz,shuffle_questions=False)	
	print(added_questions)
	q_order= [str(que.id) for que in added_questions]
	question_paper.fixed_question_order = ",".join(q_order)
	question_paper.save()
	# add fixed set of questions to the question paper
	question_paper.fixed_questions.add(*added_questions)
	question_paper.update_total_marks()
	question_paper.save()
#LESSON
    # demo_lesson = Lesson.objects.create(
    #     name="Demo lesson", description="demo lesson",
    #     html_data="demo lesson", creator=user)

#LEARNING UNIT CREATION
# quiz_units_list=['','','']
# for index, quiz_unit in enumerate(quiz_units_list, 1):
	quiz_unit =  LearningUnit.objects.create(order=index, type="quiz", quiz=quiz)
	learning_module.learning_unit.add(quiz_unit)
    
#LEARNING MODULE CREATION
course.learning_module.add(learning_module)