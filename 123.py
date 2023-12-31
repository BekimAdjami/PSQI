import streamlit as st

# Define the scoring logic for PSQI
def calculate_psqi_score(answers):
    # Component 1: Subjective sleep quality
    component_1 = answers['q9']

    # Component 2: Sleep latency
    subscore_q2 = convert_answer_to_score(answers['q2'])
    subscore_q5a = convert_answer_to_score(answers['q5a'])
    subscores_2 = [subscore_q2, subscore_q5a]
    component_2 = min(3, sum(subscores_2))

    # Component 3: Sleep duration
    component_3 = answers['q4_sleep_hours']

    # Component 4: Sleep efficiency
    bedtime_hour = int(answers['q1_bedtime_hour'])
    wakeup_hour = int(answers['q3_wakeup_hour'])
    sleep_hours = int(answers['q4_sleep_hours'])

    # Ensure denominator is not zero before performing division
    if (wakeup_hour - bedtime_hour) % 24 != 0:
        sleep_efficiency = (sleep_hours / ((wakeup_hour - bedtime_hour) % 24)) * 100
        if sleep_efficiency > 85:
            component_4 = 0
        elif sleep_efficiency > 75:
            component_4 = 1
        elif sleep_efficiency > 65:
            component_4 = 2
        else:
            component_4 = 3
    else:
        # Handle the case where the denominator is zero
        component_4 = 3

    # Component 5: Sleep disturbance
    subscores_5 = [convert_answer_to_score(answers.get(f'q5{i}', 'Не')) for i in range(2, 10)]
    component_5 = min(3, sum(subscores_5))

    # Component 6: Use of sleep medication
    component_6 = convert_answer_to_score(answers['q6'])

    # Component 7: Daytime dysfunction
    subscores_7 = [convert_answer_to_score(answers['q7']), convert_answer_to_score(answers['q8'])]
    component_7 = min(3, sum(subscores_7))

    # Global PSQI score
    global_score = component_1 + component_2 + component_3 + component_4 + component_5 + component_6 + component_7

    return global_score

# Function to convert answer to score
def convert_answer_to_score(answer):
    mapping = {
        '< 15 минути': 0,
        '16-30 минути': 1,
        '31-60 минути': 2,
        '> 60 минути': 3,
        'Не': 0,
        'Помалку од еднаш неделно': 1,
        'Eднаш или двапати неделно': 2,
        'Три или повеќе пати неделно': 3,
        'Многу добар': 0,
        'Прилично добар': 1,
        'Прилично лош': 2,
        'Многу лош': 3
    }
    return mapping.get(answer, 0)

# Streamlit app layout
st.title('Pittsburgh Sleep Quality Index (PSQI) Калкулатор')

# General information page
st.header('Општи информации')
name = st.text_input('Име:')
age = st.number_input('Возраст:', min_value=0)
work = st.text_input('Работа:')

# Navigation to the PSQI form
if st.button('Продолжи кон PSQI формата'):
    st.session_state['page'] = 'psqi_form'

# Check if we should display the PSQI form
if st.session_state.get('page') == 'psqi_form':
    # Collect user inputs for PSQI
    with st.form(key='psqi_form'):
        st.write('Инструкции: Ве молиме одговорете на сите прашања според вашите обични навици за спиење во текот на изминатиот месец.')

        # Questions 1 to 4
        q1_bedtime_hour = st.time_input('1. Во кое време обично си легнувте навечер?')
        q2_sleep_onset = st.selectbox('2. Колку време ви требаше да заспиете?', ['< 15 минути', '16-30 минути', '31-60 минути', '> 60 минути'])
        q3_wakeup_hour = st.time_input('3. Во колку часот обично станувавте наутро?')
        q4_sleep_hours = st.number_input('4. Колку часа вистински спиевте ноќе?', min_value=0)

        # Questions 5a to 5j
        q5a_difficulty_falling_asleep = st.selectbox('5a. Не можевте да заспиете во рок од 30 минути', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5b_waking_up = st.selectbox('5b. Се разбудивте среде ноќ или рано наутро', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5c_toilet_visits = st.selectbox('5c. Моравте да станете за да користите тоалет', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5d_breathing = st.selectbox('5d. Не можевте да дишете удобно', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5e_cough_snore = st.selectbox('5e. Сте кашлале или хрчеле гласно', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5f_cold = st.selectbox('5f. Сте чуствувале студ', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5g_heat = st.selectbox('5g. Сте чуствувале жештина', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5h_nightmares = st.selectbox('5h. Сте имале лоши соништа', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5i_pain = st.selectbox('5i. Сте чуствувале болка', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q5j_other_reasons = st.text_input('5j. Други причини, ве молам опишете:')

        # Questions 6 and 7
        q6_sleep_medication = st.selectbox('6. Колку често сте земале лекови за спиење?', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])
        q7_staying_awake = st.selectbox('7. Колку често сте имале потешкотии да останете будни?', ['Не', 'Помалку од еднаш неделно', 'Eднаш или двапати неделно', 'Три или повеќе пати неделно'])

        # Question 8
        q8_enthusiasm = st.selectbox('8. Колку ви беше проблем да продолжите со доволно ентузијазам за да ги завршите работите?', ['Немав потешкотии воопшто', 'Само многу лесни потешкотии', 'Средно тешки потешкотии', 'Големи потешкотии'])

        # Question 9
        q9_sleep_quality = st.selectbox('9. Како би го оцениле целокупниот квалитет на вашиот сон?', ['Многу добар', 'Прилично добар', 'Прилично лош', 'Многу лош'])

        # Question 10 (does not contribute to the score)
        q10_partner_or_roommate = st.selectbox('10. Дали имате партнер во кревет или цимер во соба?', ['Немам партнер во креветот или цимер', 'Цимер во друга соба', 'Цимер во иста соба но различен кревет', 'Партнер во ист кревет'])

        # Submit button
        if st.form_submit_button(label='Испрати'):
            answers = {
                'q1_bedtime_hour': q1_bedtime_hour.hour + q1_bedtime_hour.minute / 60,
                'q2': q2_sleep_onset,
                'q3_wakeup_hour': q3_wakeup_hour.hour + q3_wakeup_hour.minute / 60,
                'q4_sleep_hours': q4_sleep_hours,
                'q5a': q5a_difficulty_falling_asleep,
                'q5b': q5b_waking_up,
                'q5c': q5c_toilet_visits,
                'q5d': q5d_breathing,
                'q5e': q5e_cough_snore,
                'q5f': q5f_cold,
                'q5g': q5g_heat,
                'q5h': q5h_nightmares,
                'q5i': q5i_pain,
                'q5j': q5j_other_reasons,
                'q6': q6_sleep_medication,
                'q7': q7_staying_awake,
                'q8': q8_enthusiasm,
                'q9': q9_sleep_quality
                # No need to add q10 as it does not contribute to the score
            }

            # Store answers in session state
            st.session_state['answers'] = answers

# Calculate and display the PSQI score
if 'answers' in st.session_state:
    answers = st.session_state.answers

    # Calculate the sum of components for questions 5b to 5i
    sleep_disturbance_sum = sum([int(answers[f'q5{i}']) for i in range(2, 10) if f'q5{i}' in answers])
    # Convert answers to numerical values
    def convert_answer_to_score(answer):
        mapping = {
            '< 15 минути': 0,
            '16-30 минути': 1,
            '31-60 минути': 2,
            '> 60 минути': 3,
            'Не': 0,
            'Помалку од еднаш неделно': 1,
            'Eднаш или двапати неделно': 2,
            'Три или повеќе пати неделно': 3,
            'Многу добар': 0,
            'Прилично добар': 1,
            'Прилично лош': 2,
            'Многу лош': 3
        }
        return mapping.get(answer, 0)

    # Apply conversion to relevant answers
    for key in ['q5a', 'q6', 'q7', 'q8', 'q9']:
        answers[key] = convert_answer_to_score(answers[key])

    psqi_score = calculate_psqi_score(answers)
    st.write(f'Вашиот PSQI резултат е: **{psqi_score}**')
    if psqi_score <= 5:
        st.write('Вашиот сон е класифициран како добар.')
    elif 6 <= psqi_score <= 10:
        st.write('Вашиот сон е класифициран како просечен.')
    else:
        st.write('Вашиот сон е класифициран како лош.')
