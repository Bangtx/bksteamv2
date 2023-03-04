import moment from "moment/moment";
export const firstday = moment(new Date()).day(-30).format('YYYY-MM-DD');

export const lastday = moment(new Date()).format('YYYY-MM-DD');