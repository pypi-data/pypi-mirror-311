const getPwd = () => {
    // get pwd from local storage
    const pwd = localStorage.getItem('pwd');
    return pwd;
}

const savePwd = (pwd) => {
    // get pwd from local storage
    localStorage.setItem('pwd', pwd);
}

const removePwd = ()=>{
    localStorage.removeItem('pwd'); 
}

export {
    getPwd, 
    savePwd, 
    removePwd, 
}