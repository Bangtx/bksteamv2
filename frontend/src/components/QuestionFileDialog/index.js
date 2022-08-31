import moment from "moment";


export const QUESTION_INIT = {
    date: moment(new Date()).format('YYYY-MM-DD'),
    deadline: null,
    classroom: null,
    unit: null,
    description: null,
    file_url: null,
    is_global: true,
    have_to_do: false,
    student_ids: []
}