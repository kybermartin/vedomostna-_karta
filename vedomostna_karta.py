from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel)
from random import shuffle, randint


class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        # all the lines must be given when creating the object, and will be recorded as properties
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


questions_list = [] 
questions_list.append(Question('Aký je národný jazyk v Brazílii', 'Portugalčina', 'Brazilčina', 'Španielčina', 'Taliančina'))
questions_list.append(Question('Ktorú farbu neobsahuje americká zástava?', 'Zelenú', 'Červenú', 'Bielu', 'Modru'))
questions_list.append(Question('Vyberte najvhodnejší anglický názov pre koncepciu programovania na uloženie niektorých údajov', 'variable', 'variation', 'variant', 'changing'))


app = QApplication([])


btn_OK = QPushButton('Odpoveď') # answer button
lb_Question = QLabel('Najťašia otázka na svete!') # question text


RadioGroupBox = QGroupBox("Možnosti odpovede") # on-screen group for radio buttons with answers


rbtn_1 = QRadioButton('Odpoved 1')
rbtn_2 = QRadioButton('Odpoved 2')
rbtn_3 = QRadioButton('Odpoved 3')
rbtn_4 = QRadioButton('Odpoved 4')


RadioGroup = QButtonGroup() # this groups the radio buttons so we can control their behavior
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)


layout_ans1 = QHBoxLayout()   
layout_ans2 = QVBoxLayout() # the vertical ones will be inside the horizontal one 
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) # two answers in the first column
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) # two answers in the second column
layout_ans3.addWidget(rbtn_4)


layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) # put the columns in the same line


RadioGroupBox.setLayout(layout_ans1) # a “panel” with the answer options is ready 


AnsGroupBox = QGroupBox("Test odpovede")
lb_Result = QLabel('Je tvoja odpoveď správna alebo nesprávna?') # “correct” or “incorrect” will be written here
lb_Correct = QLabel('Tvoja odpoveď bude tu!') # the correct answer text will be written here


layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)


layout_line1 = QHBoxLayout() # question
layout_line2 = QHBoxLayout() # answer options or test result
layout_line3 = QHBoxLayout() # "Answer" button


layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)   
layout_line2.addWidget(AnsGroupBox)  
AnsGroupBox.hide() # hide the answer panel because the question panel should be visible first 


layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2) # the button must be large
layout_line3.addStretch(1)


layout_card = QVBoxLayout()


layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) # spaces between the contents


def show_result():
    '''zobrazi panel odpovedi  '''
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Ďalšia otázka')


def show_question():
    ''' zobrazi panel otazky '''
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Odpoveď')
    # clear selected radio button
    RadioGroup.setExclusive(False) # remove the limits so we can reset the radio buttons 
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True) # reset the limits so that only one radio button can be selected at a time 


answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]


def ask(q: Question):
    ''' funkcia vytvori otázku a náhodne usporiada možnosti '''
    shuffle(answers) # shuffle the list of buttons; now a random button is first in the list
    answers[0].setText(q.right_answer) # fill the first element of the list with the correct answer and the other elements with incorrect answers
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question) # question
    lb_Correct.setText(q.right_answer) # answer
    show_question() # show the question panel 


def show_correct(res):
    ''' ukáže odpoved - vloži a úkaže odpoveď v paneli odpovede '''
    lb_Result.setText(res)
    show_result()


def check_answer():
    ''' ak je vybraná odpoveď, skontroluje a ukáže panel odpovedi '''
    if answers[0].isChecked():
        # a correct answer!
        show_correct('Správne!')
        window.score += 1
        print('Štatistika\n-Počet otázok: ', window.total, '\n-Správne odpovede: ', window.score)
        print('Úspešnosť: ', (window.score / window.total * 100), '%')

    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            # an incorrect answer!
            show_correct('Nesprávne!')


def next_question():
    ''' ďalšia otázka zo zoznamu '''
    window.total += 1
    print('Štatistika\n-Počet otázok: ', window.total, '\n-Správne odpovede: ', window.score)

    # vytvorime lokalnu premennu kedze pri kazdom volani funkcie bude mat inu hodnotu 
    cur_question = randint(0, len(questions_list) - 1) # move on to the next question 
    q = questions_list[cur_question] # take a question
    ask(q) # ask it


def click_OK():
    ''' Toto určuje, či sa má zobraziť ďalšia otázka alebo skontrolovať odpoveď na túto otázku. '''
    if btn_OK.text() == 'Odpoveď':
        check_answer() # check the answer
    else:
        next_question() # next question


window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Vedomostná karta')

btn_OK.clicked.connect(click_OK)  

window.score = 0
window.total = 0
next_question()
window.resize(400, 300)
window.show()
app.exec()
