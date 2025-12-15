# run.py
import my_module

#import my_module  # my_module 실행. 현재 실행 모듈(run.py)와 같은 디렉토리(패키지)에서 찾는다.
#import my_package.todo_module as todo  # import my_package.todo_module 대신 todo 사용.

#from my_package import todo_module  # as todo

from my_module import *

print(plus(100, 200))

#def plus():
#    print("run의 plus")

#plus()
#todo_module.plus(100)


#r = my_module.plus(100, 200)  # module.함수()
#print(r)
#r = my_module.minus(230, 100)
#print(r)


#my_package.todo_module.print_gugudan(5)
#todo.print_gugudan(8)

# plus
# python run.py