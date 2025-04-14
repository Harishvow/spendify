from backend import *
def signout():
    st.session_state.logged_in = False

auth = ProtobaseAuth("RD3qVwq5QOEEh-b-f7oHHKu33tbLH4XylFNUuAgia_kL6GQaE06l9zxoP7h0Rk6ecStrNbf9D3ak2jOvqPmyyg")

def app():


    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            y = auth.login(email,username,password)
            if y['status-code'] != 400:
                if y['message'] == "User Successfully Logged in":
                    st.session_state.signedout = True
                    st.session_state.signout = True
                    st.session_state.username = username
                    st.session_state.useremail = email

                else:
                    st.error("Wrong Password")

            else:
                st.error("Wrong Username")

        except Exception as e:
            st.error(e)

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ""
        st.session_state.useremail = ""


    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]:
        left_co, cent_co, last_co = st.columns([3, 7, 3])

        with cent_co:
            st.title("Your :red[Account] in :green[Spendify]")

            choice = st.radio('Login/Signup', ['Login', 'Sign up'],
                              horizontal=True,
                              label_visibility="hidden",
                              index=1,
                              key="radios")

            email = st.text_input("E-mail", key="new_usern")
            username = st.text_input('Username', key="log_usern")
            password = st.text_input('Password', type='password')

            if choice == 'Sign up':
                if st.button('Create my account', use_container_width=True):
                    if username != "" and password != "":
                        x = auth.signup(email, username, password)
                        if x["status-code"] == 200:
                            st.success("Account Created Successfully")
                            st.session_state.signedout = True
                            st.session_state.signout = True
                            st.session_state.username = username
                            st.session_state.useremail = email
                    else:
                        st.error(":red[No empty fields please]")

            else:
                st.button('Login', on_click=f, use_container_width=True)

    if st.session_state.signout:

        left_co, cent_co, last_co = st.columns([3, 7, 3])

        with cent_co:
            st.title("Your :red[Account] in :green[$pend It.]")
            st.markdown("#")

            with st.container(border=0):
                st.info(f'Username :  {str(st.session_state.username)}')
                st.info(f'E-Mail :  {str(st.session_state.useremail)}')
                st.button('Sign out', on_click=t, use_container_width=True)