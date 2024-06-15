import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}
// persist_storage 상태 변수 정의
// 해당 함수는 상태 변수를 로컬 스토리지에 저장하여 페이지가 새로고침되거나 닫혔다가 다시 열려도 데이터가 유지되도록 한다.
export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword","")
export const access_token = persist_storage("access_token", "") //액세스 토큰 저장 , 기본값은 빈 문자열
export const username = persist_storage("username", "") // 사용자 이름 저장, 기본값은 빈 문자열
export const is_login = persist_storage("is_login", false) // 로그인 상태 여부 저장, 기본값은 false