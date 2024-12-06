import "./style.scss";
import {
  Row,
  Col,
  Button,
  Table,
  Space,
  Avatar,
  Anchor,
  Card,
  ConfigProvider,
  Input,
} from "antd";
import { PictureFilled, DownOutlined, CloseOutlined, PlayCircleOutlined, CaretDownOutlined } from "@ant-design/icons";
import { useFetcher, useLocation, useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";

import DeleteSvg from "@/assets/svg/delete.svg";

import MySelectPopover from "@/components/SelectPopover";
import { addProcess, 
  checkPwd, 
  deleteProcess, 
  downloadObject, 
  getEnvOptions, 
  getLogs, getObjects, 
  getScripts, loadProjectEnvs, 
  loadProjectInfo, removeObj, runProject, setMainScriptDB, setProcessEnv, 
  setProcessScript, setProjectName, streamLogs, 
  terminateRun} from "../../backend/networking";
import { getPwd } from "../../backend/security";

// Images
import code_file from "@/assets/images/document_code.png";

const anchorList = [
  {
    title: "General",
    href: "#title-1",
  },
  {
    title: "Main script",
    href: "#title-2",
  },
  {
    title: "Running processes",
    href: "#title-3",
  },
  {
    title: "Logs",
    href: "#title-4",
  },
  {
    title: "Object generated",
    href: "#title-5",
  },
];

const PageLeftAnchor = () => {
  const location = useLocation();
  let hash = location.hash;
  if (hash.length === 0) {
    hash = anchorList[0].href;
  }

  return (
    <>
      <ul className="my-anchor-list">
        {anchorList.map((item, index) => (
          <li key={index} className={hash === item.href ? "active" : ""}>
            <Anchor.Link href={item.href} title={item.title} />
          </li>
        ))}
      </ul>
    </>
  );
};

const CardContent3 = ({
  projectID
}) => {

  {/* Data for running processes */}
  const [tableData, setTableData] = useState([
    {
      key: "1",
      value1: "Lorem Ipssedwduasdwdwedwehduewheduiheqm",
      value2: "XXXXXX",
      value3: "XXXXXX",
    },
  ]);

  const [projEnvs, setProjEnvs] = useState([]); 

  const [envOptions, setEnvOptions] = useState([]); 

  const [scriptOptions, setScriptOptions] = useState([]);

  const addOneProcessUI = ()=> {
    setTableData([
      ...tableData, 
      {
        key: `${tableData.length}`,
        value1: null,
        value2: null,
        value3: null,
      }
    ])
  }

  const onClick = ()=>{
    addOneProcessUI();
    addProcess(projectID).then((value)=>{
      loadEnvs(); 
    })
  }



  const processEnvs = (value)=>{
    setProjEnvs(value.envs);;
    setTableData(value.envs.map((item, index)=>({
      key: `${index}`,
      value1: item.name,
      value2: item.script_name,
      value3: item.create_time,
    })))
  }

  const loadEnvs = async ()=> {
    loadProjectEnvs(projectID).then(processEnvs);
  }

  const chooseEnvDone = (index,value)=>{
    const updatedTableData = [...tableData];
    updatedTableData[index].value1 = value.name; // Update the correct field
    setTableData(updatedTableData);
    console.log(projEnvs[index])
    console.log(value);
    const targetProjectEnvID = projEnvs[index].id; 
    const targetEnvID = value.env_id;
    setProcessEnv(targetProjectEnvID, targetEnvID).then((value)=>{
      reload(); 
    })
  }

  const processEnvOptions = (value)=> {
    setEnvOptions(value.envs)
  }

  const loadEnvOptions = async ()=> {
    getEnvOptions().then(processEnvOptions); 
  }

  const chooseScriptDone = (index, value)=>{
    const updatedTableData = [...tableData];
    updatedTableData[index].value2 = value.name; // Update the correct field
    setTableData(updatedTableData);
    const targetProjectEnvID = projEnvs[index].id; 
    const targetScriptID = value.script_id;
    setProcessScript(targetProjectEnvID, targetScriptID).then((value)=>{
      reload(); 
    }); 
  }

  const processScriptOptions = (value)=>{
    setScriptOptions(value.scripts);
  }

  const loadScriptOptions = ()=>{
    getScripts().then(processScriptOptions);
  }

  const onProcessDeleted = (index)=>{
    const newData = [...tableData]; 
    newData.splice(index, 1);
    setTableData(newData);
    deleteProcess(projEnvs[index].id).then((value)=> {
      reload()
    })
  }

  const reload = async ()=>{
    loadEnvs(); 
    loadEnvOptions(); 
    loadScriptOptions();
  }

  useEffect(()=>{
    reload()
  }, [])

  {/* Running processes */}
  const columns = [
    {
      title: <p style={{margin:'0', color:'#6A7081'}}>ENVIRONMENT</p>,
      dataIndex: "value1",
      key: "value1",
      render: (text, item, index) => (
        <Space size={"middle"}>

          <Avatar
            size={30}
            shape="square"
            style={{ backgroundColor: "#f08e44" }}
          >
            L
          </Avatar>

          <div className="my-card3-row-title">
            <div style={{fontSize:'1em', width:'85%', overflow:'hidden',textOverflow:'ellipsis', whiteSpace: 'nowrap'}}>{text}</div>
            <p className="my-row-attr">
              <span>8 CPU</span>
              <span>0 GPU</span>
              <span>10 data</span>
              <span> 10 GB</span>
            </p>
          </div>

          <MySelectPopover placement="bottomRight" elements={envOptions} 
          complete={(value)=>{
              chooseEnvDone(index, value)
            }}>
            <Button color="default" variant="filled" icon={<DownOutlined />} />
          </MySelectPopover>
        </Space>
      ),
      width:"40%"
    },
    {
      title: <p style={{margin:'0', color:'#6A7081'}}>SCRIPT</p>,
      dataIndex: "value2",
      key: "value2",
      render: (text, item, index) => (
        <Space size={"middle"}>
          <Avatar size={30} shape="square" style={{backgroundColor:'transparent'}}>
            <img src={code_file} alt="" />
          </Avatar>
          <div
            className="text-line-1-ellipsis my-card3-row-title"
            style={{ width: "150px" }}
          >
            {text}
          </div>
          <MySelectPopover placement="bottomRight" elements={scriptOptions} 
          complete={(value)=>{
              chooseScriptDone(index, value)
            }}>
            <Button color="default" variant="filled" icon={<DownOutlined />} />
          </MySelectPopover>
        </Space> // Dropdown
      ),
      width:'30%'
    },
    {
      title: <p style={{margin:'0', color:'#6A7081'}}>CREATED AT</p>,
      dataIndex: "value3",
      key: "value3",
    },
    {
      title: "",
      dataIndex: "",
      key: "",
      align: "center",
      render: (text, item, index) => (
        <button className="button-remove-running-process">
          <img
            src={DeleteSvg}
            alt="delete"
            style={{ color: "#b5b8c0", cursor: "pointer" }}
            onClick={()=>{onProcessDeleted(index)}}
          />
      </button>
      ),
    },
  ];

  return (
    <Card
      id="title-3"
      title={<span className="my-card-title">Running processes</span>}
      extra={
        <Button color="primary" variant="filled" onClick={onClick}>
          Add new
        </Button>
      }
      className="my-card-custom"
    >
      <Table
        dataSource={tableData}
        columns={columns}
        pagination={{ position: [] }}
      />
    </Card>
  );
};


const CardContent5 = ({
  projectID
}) => {
  const [tableData, setTableData] = useState([
    
  ]);

  const [objects, setObjects] = useState([]);

  const onDeletedItem = async (index) => {
    console.log(index);
    console.log(tableData[index])
    removeObj(tableData[index].key).then((value)=>{
      loadObjects(); 
    })
    setTableData([...tableData.filter((value, idx)=> index!=idx)])
  }
  

  const columns = [
    {
      title: <p style={{margin:'0', color:'#6A7081'}}>OBJECT</p>,
      dataIndex: "value1",
      key: "value1",
      render: (text) => 
        <p style={{fontSize:'.95em', fontWeight:'400'}}>
          {text}
        </p>,
      width: '30%'
    },
    {
      title: <p style={{margin:'0', color:'#6A7081'}}>TYPE</p>,
      dataIndex: "value2",
      key: "value2",
      render: (text) => 
        <p style={{fontSize:'.95em', fontWeight:'400', width:'100%', textOverflow:'hidden'}}>
          {text}
        </p>,
      width: '30%'
    },
    {
      title: <p style={{margin:'0', color:'#6A7081'}}>CREATED AT</p>,
      dataIndex: "value3",
      key: "value3",
      render: (text) => 
        <p style={{fontSize:'.95em', fontWeight:'400'}}>
          {text}
        </p>,
      width: '30%'
    },
    {
      title: "",
      dataIndex: "",
      key: "",
      align: "center",
      render: (text, item, index) => (
        <button className='remove-object-button' onClick={(e)=>{
          e.stopPropagation(); 
          onDeletedItem(index)
        }} ><CloseOutlined className='icon' /></button>
      ),
    },
  ];


  const downloadItem = (index) => {
    downloadObject(tableData[index].key); 
  }

  

  const processObjects = (value)=> {
    setObjects(value.objects); 
    console.log(value);
    setTableData(value.objects.map((item,index)=>({
      key: item.object_id,
      value1: item.name,
      value2: item.object_type,
      value3: item.create_time,
    })))
  }

  const loadObjects = async () => {
    getObjects(projectID).then(processObjects); 
  }

  useEffect(()=>{
    loadObjects(); 
  },[])
  

  return (
    <Card
      id="title-5"
      title={<span className="my-card-title">Object generated</span>}
      className="my-card-custom"
    >
      <Table
        dataSource={tableData}
        columns={columns}
        rowClassName={() => "my-table-row-custom"}
        pagination={{ position: [] }}
        onRow={(record, rowIndex) => {
          return {
            onClick: () => {
              console.log("Clicked!", rowIndex); // Click object
              downloadItem(rowIndex); 
            },
        }}}
      />
    </Card>
  );
};

const PageRightContent = ({
  projectID
}) => {
  const [inputValue1, setInputValue1] = useState("Lorem Ipsum is simply dummy text of the");
  const [originalValue1, setOriginalValue1] = useState(inputValue1);
  const [logs, setLogs] = useState([]); 
  const [running, setRunning] = useState(true); 
  const [streamCounter, setStreamCounter] = useState(0); 
  const [scripts, setScripts] = useState([]); 
  const [mainScript, setMainScript] = useState(''); 
  const [createTime, setCreateTime] = useState(''); 

  const handleInputChange1 = (e) => {
    setInputValue1(e.target.value);
  };

  const handleInputBlur1 = () => {
    if (inputValue1.trim() === "") {
      setInputValue1(originalValue1);
    } else {
      setOriginalValue1(inputValue1);
      setProjectName(projectID, inputValue1).then((value)=>{
        loadInfo(); 
      });
    }
  };

  const processInfo = (value)=> {
    const basicInfo = value.basic_info; 
    console.log('basic info'); 
    console.log(basicInfo); 
    setInputValue1(basicInfo.name); 
    setMainScript(basicInfo.main_script); 
    setCreateTime(basicInfo.update_time); 
  }

  const loadInfo = async ()=>{
    loadProjectInfo(projectID).then(processInfo);
  }

  const processLogs = (value)=>{
    setLogs(value.logs); 
  }

  const loadLogs = async ()=>{
    getLogs(projectID).then(processLogs); 
  }

  const loadScripts = async () =>{
    getScripts().then((value)=>{
      setScripts(value.scripts); 
    });
  }

  const getMainName = ()=>{
    try{
      return scripts.filter((item)=>item.script_id===mainScript)[0].name;
    }catch(e){
      return ''; 
    }
  }

  const clickRun = async () => {
    if(running ===false){
      setRunning(true);
      setLogs([]);
      runProject(projectID).then((value)=>{
        loadInfo(); 
        setStreamCounter((prev)=>prev+1); 
      }); 
    }else{
      stopProject()
    }
    
  }

  const completeChooseScript = (item)=>{
    setMainScript(item.script_id); 
    setMainScriptDB(projectID, item.script_id); 
  }


  const streamLogs1 = async () => {

    var currentLogs = [...logs]; 

    console.log('streaming:');
    console.log(running);

    while (running===true){
      console.log('running');
      try{
        const res = await streamLogs(projectID, currentLogs.length); 
        console.log('some result');
        console.log(res);
        if(res.running==false){
          setRunning(false); 
          break; 
        }
        currentLogs = [...currentLogs, ...res.logs]; 
        setLogs([...currentLogs]);
        if(res.logs.length==0){
          await new Promise(resolve => setTimeout(resolve, 1000));
          continue;
        }
        continue; 
      }catch(e){
        console.log(e); 
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    loadLogs();
  }


  const streamRun = async ()=>{
    const res = await streamLogs(projectID, logs.length); 
    console.log('res');
    console.log(res);
    setRunning(res.running); 
    if(res.running===false){
      loadLogs(); 
      return; 
    }
    try{
      setLogs((prev)=>[...prev, ...res.logs]); 
    }catch(e){}
    if(res.logs.length > 0){
      setStreamCounter((prev)=>prev+1); 
    }else{
      await new Promise(resolve => setTimeout(resolve, 1000));
      setStreamCounter((prev)=>prev+1);
    }
  }

  const stopProject = ()=>{
    setRunning(false); 
    terminateRun(projectID).then((value)=>{
      loadInfo(); 
      loadLogs(); 
    }); 
  }

  useEffect(()=>{
    streamRun();
  }, [streamCounter,]);
  

  useEffect(()=>{
    loadInfo(); 
    streamLogs1(); 
    loadScripts(); 
  },[1,]);

  return (
    <>


      <Card
        id="title-1"
        title={<span className="my-card-title">General</span>}
        className="my-card-custom"
      >
        <div className="my-drawer-top-item">
          <span className="my-drawer-top-item-label">Project </span>
          <ConfigProvider
            theme={{
              components: {
                Input: {
                  hoverBorderColor: "rgba(204, 207, 216)",
                },
              },
              token: {
                colorBorder: "transparent",
              },
            }}
          >
            <Input 
              value={inputValue1}
              onChange={handleInputChange1}
              onBlur={handleInputBlur1}
            />
          </ConfigProvider>
        </div>
        <div className="my-drawer-top-item">
          <span className="my-drawer-top-item-label">Created at</span>
          <ConfigProvider
            theme={{
              components: {
                Input: {
                  hoverBorderColor: "rgba(204, 207, 216)",
                },
              },
              token: {
                colorBorder: "transparent",
              },
            }}
          >
            <Input value={createTime} />
          </ConfigProvider>
        </div>
      </Card>

      <Card
        id="title-2"
        title={<span className="my-card-title">Main script</span>}
        className="my-card-custom"
      >
        <div className="my-drawer-top-item">
          <span className="my-drawer-top-item-label">Choose a file</span>
          <ConfigProvider
            theme={{
              components: {
                Input: {
                  hoverBorderColor: "rgba(204, 207, 216)",
                  
                },
              },
            }}
          >
            <Input placeholder={`File name: ${getMainName()}`} style={{pointerEvents:'none'}} />

            {/* Choose a file { */}
          <div style={{position:'absolute', right:'24px'}}>
            <MySelectPopover 
                placement="bottomRight" 
                elements={scripts.filter((item)=>item.script_id!==mainScript)} 
                complete={completeChooseScript}
              >

              <Button color="default" variant="filled" icon={<DownOutlined />} style={{width:'100px', borderRadius:'0px 4px 4px 0px'}} />

            </MySelectPopover>
          </div>
          {/* Choose a file { */}
          </ConfigProvider>
        </div>
      </Card>

      <CardContent3 projectID={projectID}></CardContent3>

      <Card
        id="title-4"
        title={<span className="my-card-title">Logs</span>}
        extra={
          <Button variant="filled" style={{backgroundColor:'#497BFD', color:'#fff', border:'none'}} onClick={clickRun}>
            <PlayCircleOutlined />
            { running?"Stop Running":"Run the project"}
          </Button>
        }
        className="my-card-custom"
      >
       <div
          style={{
            height: "400px",
            backgroundColor: "#000",
            color: "#fff",
            overflowY: "auto",
            padding: "10px",
            lineHeight: "1",
            borderRadius: '5px'
          }}
        >
          {
            logs.map((item,index)=>(<p>{item}</p>))
          }
        </div>
      </Card>

      <CardContent5 projectID={projectID}></CardContent5>
    </>
  );
};






const Page11 = () => {

  const navigate = useNavigate();

  useEffect(()=>{
    checkPwd(getPwd()).then((val)=>{
      if(val.match===false){
        navigate('/login'); 
      }
    })
  }, [])


  const location = useLocation();
  const key = location.search ? new URLSearchParams(location.search).get('key') : null;

  const processInfo = (value)=> {
    console.log(value);
  }

  const loadInfo = async ()=>{
    loadProjectInfo(key).then(processInfo);
  }

  useEffect(()=>{
    loadInfo(); 
  },[])

  return (
    <>
      <Row justify="center" align="middle" style={{ height: "100%" }}>
        <Col span={22} style={{ height: "100%" }}>
          <Row justify="center" align="middle" style={{ height: "100%" }}>
            <Col
              span={6}
              style={{
                height: "100%",
                overflow: "auto",
              }}
            >
              <div style={{height:'25px'}}></div>
              <PageLeftAnchor />
            </Col>
            <Col
              span={18}
              style={{
                height: "100%",
                overflow: "auto",
              }}
              className="right-content"
            >
              
              <PageRightContent projectID={key} ></PageRightContent>
              <div style={{height:'55px'}}></div>
            </Col>
          </Row>
        </Col>
      </Row>
    </>
  );
};

export default Page11;
