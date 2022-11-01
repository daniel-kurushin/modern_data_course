class Human:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f"Human('{self.name}')"

class Student(Human):
	def __repr__(self):
		return f"Student('{self.name}')"

class Classes:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f"Classes('{self.name}')"

class Lecture(Classes):
	def __repr__(self):
		return f"Lecture('{self.name}')"

class Practice(Classes):
	def __repr__(self):
		return f"Practice('{self.name}')"

class Discipline:
	def __init__(self, 
		         name, 
		         lectures=[],
		         practices=[],
		         teacher=None,
		         students=[]):
		self.name = name
		self.lectures = lectures
		self.practices = practices
		self.teacher = teacher
		self.students = students

	def __repr__(self):
		return f"Discipline('{self.name}, ...')"

class Teacher(Human):
	def __repr__(self):
		return f"Teacher('{self.name}')"

	def receive_report(self, report):
		try:
			self.reports += [report]
		except AttributeError:
			self.reports = [report]

	def enum_reports(self):
		for x in self.reports:
			yield x

class Report:
	def __init__(self, 
		         name,
		         student,
		         practice):
		self.name = name
		self.student = student
		self.practice = practice

	def __repr__(self):
		return f"Report('{self.name}', ...)"

if __name__ == '__main__':
	human = Human('Вася')
	lena = Student('Лена')
	alex = Teacher('Александр')
	lecture1 = Lecture('Введение в Python')
	lecture2 = Lecture('Типы данных в Python')
	practice1 = Practice('Посчитать сумму ряда')
	practice2 = Practice('Посчитать avg(ряда)')
	python = Discipline(
		name      = 'Основы Python',
		lectures  = [lecture1, lecture2],
		practices = [practice1, practice2],
		teacher   = alex,
		students  = [lena])
	a_report = Report(
		name = 'Посчитать сумму ряда A',
		student = lena,
		practice = practice1)
	b_report = Report(
		name = 'Посчитать сумму ряда B',
		student = lena,
		practice = practice2)
	alex.receive_report(a_report)
	alex.receive_report(b_report)
	print(list(alex.enum_reports()))
