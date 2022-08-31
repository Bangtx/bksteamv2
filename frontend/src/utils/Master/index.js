import { api, i18n } from '@/plugins'
import { endpoints } from '@/utils'

export const toYomi = async (text) => {
    try {
        const response = await api.get(`${endpoints.TO_YOMI}?text=${text}`)
        return response.data
    } catch (err) {
        console.log(err)
    }
    return null
}

export const actionDotsVertical = [
    {
        id: 1,
        text: 'common.update',
        icon: 'mdi-pencil',
        action: 'on-update',
        disabled: false,
        color: 'blue'
    },
    {
        id: 2,
        text: 'common.delete',
        icon: 'mdi-delete-empty',
        action: 'on-delete',
        disabled: false,
        color: 'red'
    }
]

export const moveCursor = (event, $refs, list_states, focusInput, groupRefName=null) => {
    /*
    * event: keydown event
    * list_states: array reference name exp ['code', 'untg', 'name', 'yomi', 'name_short', 'name_eng']
    * focusInput: reference name is focusing exp name
    * groupRefName: str reference name select tag group exp keyGroup of unit_group is 'untg', size_group is 'sizg'
    * */
    let index = list_states.findIndex(sates => sates === focusInput)
    if ((event.keyCode === 13 || event.keyCode === 9) && index !== list_states.length - 1)
        focusInput = list_states[index + 1]

    // if tab button not neet next cursor focus
    if (event.keyCode !== 9) {
        if ($refs[focusInput]) $refs[focusInput]?.focus()
        else {
            $refs.master_dialog.$refs[focusInput]?.focus()
            if (groupRefName) $refs[groupRefName]?.blur()
        }
    }

    return focusInput
}


export const getErrorMessage = (error, toast) => {
    let msg = []
    if (error.response?.data?.detail?.length > 0) {
        error.response?.data?.detail.forEach((e) => {
            const {error_code, duplicate} = e
            toast.error(i18n.t(`error_code.${e?.error_code}`))
            msg.push(i18n.t(`error_code.msg_${error_code}`, {group: duplicate.group_name, name: duplicate?.name}))
        })
    }
    return msg
}