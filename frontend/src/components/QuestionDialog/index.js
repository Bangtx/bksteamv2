import moment from "moment";


export const QUESTION_INIT = {
    date: moment(new Date()).format('YYYY-MM-DD'),
    deadline: null,
    classroom: null,
    question: null,
    unit: null,
    audio: null,
    multi_choice: false,
    option_1: null,
    option_2: null,
    option_3: null,
    option_4: null,
    answer: '',
    have_to_do: false
}