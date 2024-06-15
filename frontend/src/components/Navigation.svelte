<script>
    import { link } from 'svelte-spa-router'
    import { page, keyword, access_token, username, is_login } from "../lib/store"
</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <!-- 로고와 홈 링크-->
        <a use:link class="navbar-brand" href="/" on:click="{() => {$keyword ='', $page = 0}}">Pybo</a>
        <!-- 모바일 장치에서 네비게이션바를 접고 펼치는 버튼-->
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <!-- 사용자가 로그인했을 때 -->
                {#if $is_login }
                    <li class="nav-item">
                        <!--로그아웃 링크, 로그인한 사용자 이름 표시-->
                        <a use:link href="/user-login" class="nav-link" on:click={() => {
                            $access_token = ''
                            $username = ''
                            $is_login = false
                        }}>로그아웃 ({$username})</a>
                        <!--로그아웃 링크를 눌렀을 때 스토어에 저장했던 값들을 초기화-->
                    </li>
                {:else}
                    <!-- 사용자가 로그인하지 않았을 때-->
                    <li class="nav-item">
                        <!--회원 가입 링크-->
                        <a use:link class="nav-link" href="/user-create">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <!-- 로그인 링크-->
                        <a use:link class="nav-link" href="/user-login">로그인</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>