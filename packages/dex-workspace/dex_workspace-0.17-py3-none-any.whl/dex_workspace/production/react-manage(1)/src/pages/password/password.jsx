import { useEffect, useState } from 'react';
import { Layout } from "antd";


// SCSS
import style from "./password.module.scss";
import { getPwd, removePwd, savePwd } from '../../backend/security';
import { checkPwd } from '../../backend/networking';
import { useNavigate } from 'react-router-dom';

// Images
import logo from "@/assets/images/logo.png";

const Password_PAGE = () => {

    const navigate = useNavigate()

    // Browser tab title
    useEffect(() => { document.title = 'Login'; }, []);

    const [pwd, setPwd] = useState(''); 

    const onPwdChange = (event) =>{
        setPwd(event.target.value); 
    }

    const onPwdCheck = (val)=>{
        if(val.match===true){
            savePwd(pwd); 
            navigate('/')
        }
    }

    const onLogin = ()=>{
        if(pwd!==''){
            checkPwd(pwd).then(onPwdCheck)
        }
       /*removePwd(); 
       console.log(getPwd());*/
    }

    return(
        <>
        
        <Layout className={style.main}>


            <div className={style.center}>

                {/* Column of content ------{ */}
                <div className={style.canvas}>

                    <div className={style.logo}>
                        <img src={logo} alt="" style={{width:'100%'}} />
                    </div>

                    <h1>Make AI data collaboration <br/> easy and safe</h1>


                    {/* Input space */}
                    <div className={style.input}>

                        <input type="text" placeholder='Type your password' onChange={onPwdChange}/>

                        <button onClick={onLogin}>Login</button>

                    </div>{/* Input space */}

                </div>{/* Column of content ------ } */}

            </div>
           
        </Layout>

        </>
    );
}

export default Password_PAGE 