<script>
    import { push } from 'svelte-spa-router' 
    import fastapi from "../lib/api" 
    import Error from "../components/Error.svelte"
    import { access_token, username, is_login } from "../lib/store"
    

    let error = {detail:[]} // 에러 메세지 저장할 변수
    let login_username = "" // 로그인 폼에서 입력받은 사용자 이름을 저장할 변수
    let login_password = "" // 로그인 폼에서 입력받은 비밀번호를 저장할 변수 

    // 로그인 함수 정의
    function login(event) {
        event.preventDefault() // 폼 제출 시 페이지 리로드 방지
        let url = "/api/user/login"
        let params = {
            username: login_username,
            password: login_password,
        }
        fastapi('login', url, params, 
            (json) => {                 // 성공 콜백 함수
                console.log("Success callback executed : ",json);
                $access_token = json.access_token
                $username = json.username
                $is_login = true
                
                
                push("/")               // 로그인 성공 시, 홈 페이지로 리다이렉트
            },
            (json_error) => {
                console.log("Error callback executed : ",json_error)           // 실패 콜백 함수
                error = json_error      // 로그인 실패 시, 에러 메시지 저장
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">로그인</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" id="username" bind:value="{login_username}">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" id="password" bind:value="{login_password}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{login}">로그인</button>
    </form>
</div>