const curr = new Date; // get current date
const first = curr.getDate() - curr.getDay() - 1 // First day is the day of the month - the day of the week
const last = first + 6; // last day is the first day + 6
 
export const firstday = new Date(curr.setDate(first)).toUTCString()
export const lastday = new Date(curr.setDate(last)).toUTCString()