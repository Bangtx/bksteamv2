import router from '@/router'

export const replaceUrl = ({query, params}) => {
    // type query and params is object
    // exp: {id: 1}
    router
        .replace({
            query: query,
            params: params
        })
        .catch((e) => {
            console.log(e)
        })
}