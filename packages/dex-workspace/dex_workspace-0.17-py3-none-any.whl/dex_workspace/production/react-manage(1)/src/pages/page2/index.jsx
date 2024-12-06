import "./style.scss";
import {
  Row,
  Col,
  Flex,
  Button,
  Input,
  Select,
  Table,
  ConfigProvider,
  Space,
  Avatar,
  Drawer,
  Tag,
} from "antd";
import {
  PlusCircleOutlined,
  SearchOutlined,
  PictureFilled,
  ArrowRightOutlined,
  CloseOutlined,
} from "@ant-design/icons";

import { useEffect, useId, useState } from "react";

import {checkPwd, deleteScript, getScripts, handleScriptUpload, renameScript, updateScript} from "../../backend/networking";

import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { getPwd } from "../../backend/security";
import { useNavigate } from "react-router-dom";

// Images
import file_avatar from "@/assets/images/document_code.png";

const Page2 = () => {
  /*const [tableData, setTableData] = useState([
    {
      key: "1",
      value1: "Lorem Ipsum is simply dummy text of",
      value2: "Lorem Ipsum",
      value3: "Lorem Ipsum",
      value4: "Lorem Ipsum is simply dummy",
    },
    {
      key: "2",
      value1:
        "Lorem Ipsum is simply dummy text of the Lorem Ipsum is simply dummy text of the",
      value2: "Lorem Ipsum",
      value3: "Lorem Ipsum",
      value4: "Lorem Ipsum is simply dummy",
    },
  ]);*/

  const navigate = useNavigate();

  useEffect(()=>{
    checkPwd(getPwd()).then((val)=>{
      if(val.match===false){
        navigate('/login'); 
      }
    })
  }, [])

  const [tableData, setTableData] = useState([]);

  const [innerName, setInnerName] = useState('');
  const [innerTime, setInnerTime] = useState('');
  const [innerContent, setInnerContent] = useState(''); 

  const [searchText, setSearchText] = useState('');

  const [editingIndex, setEditingIndex] = useState(null); // Track which row is being edited
  const [editingValue, setEditingValue] = useState(''); // Track the value being edited

  const [sortOrder, setSortOrder] = useState("1");
  const [scripts, setScripts] = useState({}); 

  const [scriptIndex, setScriptIndex] = useState(0); 

  const [code, setCode] = useState("some code");

  const handleSort = (value) => {
    setSortOrder(value);
    setTableData(prev => {
      const newData = [...prev];
      return newData.sort((a, b) => {
        if (value === "1") {
          return a.value1.localeCompare(b.value1);
        } else {
          return b.value1.localeCompare(a.value1);
        }
      });
    });
  };

  const columns = [
    {
      title: "TITLE",
      dataIndex: "value1",
      key: "value1",
      render: (text, item, index) => {
        
        const updateInDB = ()=>{
          renameScript(item.key, tableData[index].value1).then(
            (value)=>{
              loadScripts(); 
            }
          );
        }
        
        return (
          <>
            {editingIndex === index ? ( // Check if this row is being edited
              <Input
                readOnly={true}
                value={editingValue}
                onChange={(e) => setEditingValue(e.target.value)} // Update editing value
                onBlur={() => {
                  setTableData((prevData) => {
                    const newData = [...prevData];
                    newData[index].value1 = editingValue; // Update the table data
                    return newData;
                  });
                  setEditingIndex(null); // Reset editing index
                  updateInDB(); 
                }}
                onPressEnter={() => { // Save on Enter key
                  setTableData((prevData) => {
                    const newData = [...prevData];
                    newData[index].value1 = editingValue; // Update the table data
                    return newData;
                  });
                  setEditingIndex(null); // Reset editing index
                  updateInDB(); 
                }}
              />
            ) : (
              <Space size={"middle"}>
                <Avatar size={35} shape="square" style={{backgroundColor:'transparent'}}>
                  <img src={file_avatar} alt="" />
                </Avatar>
                <p className="text-line-1-ellipsis" style={{ maxWidth: 400 }} onClick={() => {
                  //setEditingIndex(index); // Set the index to edit
                  //setEditingValue(text); // Set the current value for editing
                }}>
                  {text}
                </p>
              </Space>
            )}
          </>
        );
      },
      width: 380,
    },
    {
      title: "SIZE",
      dataIndex: "value2",
      key: "value2",
    },
    {
      title: "MODIFIED",
      dataIndex: "value3",
      key: "value3",
    },
    {
      title: "CREATED",
      dataIndex: "value4",
      key: "value4",
    },
    {
      title: "",
      dataIndex: "",
      key: "",
      width: 100,
      align: "center",
      render: (text, item, index) => (
        <button className="remove-file-from-table"
          onClick={(e) => {
            e.stopPropagation(); 
            console.log(item);
            deleteScript(item.key).then((value)=>{
              loadScripts(); 
            })
            setTableData((prevData) => prevData.filter((_, i) => i !== index));
            console.log("Remove this row"); 
          }}
        >
          <CloseOutlined className='icon' />
        </button>
      ),
    },
  ];

  const [openDrawer, setOpenDrawer] = useState(false);

  const onDrawerClose = () => {
    setOpenDrawer(false);
  };

  const handleRowClick = (item, index) => {
    console.log(item, index);
    setInnerName(tableData[index].value1); 
    setInnerTime(tableData[index].value3); 
    console.log(innerName, innerTime);
    setScriptIndex(index); 
    setCode(scripts[item.key].content); 
    setOpenDrawer(true);
  };

  const processScripts = (value) => {
    const updatedScripts = value.scripts.map(script => ({
      key: script.script_id,
      value1: script.name,
      value2: script.size,
      value3: script.update_time,
      value4: script.create_time,
    }));
    
    const sortedScripts = [...updatedScripts].sort((a, b) => {
      if (sortOrder === "1") {
        return a.value1.localeCompare(b.value1);
      } else {
        return b.value1.localeCompare(a.value1);
      }
    });
    
    setTableData(sortedScripts);

    setScripts((prev)=>{
      var newMap = {}; 
      for(const i of value.scripts){
        newMap[i.script_id] = i;
      }
      return newMap; 
    })
  };
  const loadScripts = async () => {
    getScripts().then(processScripts); 
  }

  useEffect(()=>{
    loadScripts(); 
  }, [])

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    handleScriptUpload(event).then((value)=>{
      loadScripts(); 
    }); 
  };

  const showContent = ()=>{
    try{
      return scripts[tableData[scriptIndex].key].content; 
    }catch(e){
      return ''; 
    }
  }


  const editCode = (value)=> {
    var usedID = tableData[scriptIndex].key; 
    setScripts((prev)=>{
      var newData = {...prev}; 
      newData[usedID].content =  value; 
      return newData; 
    });
    updateScript(value, usedID);
  }

  const onBlurScripts = (prev)=>{
    prev[tableData[scriptIndex].key].name = innerName; 
    return prev; 
  }
  const onBlurTable = (prev)=>{
    prev[scriptIndex].value1 = innerName; 
    return prev; 
  }

  const innerNameBlur = ()=>{
    if(innerName!=='' && innerName!==null){
      setScripts(onBlurScripts); 
      setTableData(onBlurTable); 
      renameScript(tableData[scriptIndex].key, innerName).then((value)=>{
        loadScripts(); 
      }); 
    }else{
      setInnerName(tableData[index].value1); 
    }
  }

  const onEditInnerName = (event)=>{
    setInnerName(event.target.value); 
  }

  return (
    <>
      <Row justify="center" align="middle">
        <Col xs={22} sm={22} md={22} lg={22} xl={20} className="page-container">

          <div style={{height:'30px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <h1>My scripts</h1>
            <Button type="primary" shape="round" icon={<PlusCircleOutlined />}>
              <input 
                type="file" 
                accept=".py" 
                style={{ display: 'none' }} 
                onChange={handleFileUpload} 
                id="file-upload" 
              />
              <label htmlFor="file-upload" style={{ cursor: 'pointer' }}>
                Add new script
              </label>
            </Button>
          </Flex>

          <div style={{height:'20px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <Select
              defaultValue="1"
              style={{ width: 150 }}
              options={[
                { value: "1", label: "A - Z" },
                { value: "2", label: "Z - A" },
              ]}
              onChange={handleSort}
              value={sortOrder}
            />

            <Input
              placeholder="Search"
              style={{ width: 200 }}
              prefix={<SearchOutlined style={{ color: "rgba(0,0,0,0.45)" }} />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
            />
          </Flex>

          <ConfigProvider
            theme={{
              components: {
                Table: {
                  headerBg: "rgba(237, 239, 243)",
                  headerColor: "rgba(106, 112, 129)",
                  borderColor: "rgba(225, 228, 232)",
                },
              },
            }}
          >
            <Table
              dataSource={tableData.filter((value)=> value.value1.toLowerCase().includes(searchText.toLowerCase()))}
              columns={columns}
              style={{
                marginTop: 30,
                marginBottom: 20,
              }}
              rowClassName={() => "my-table-row-custom"}
              pagination={{ position: [], pageSize: 50}}
              onRow={(record, rowIndex) => {
              return {
                onClick: () => {
                  handleRowClick(record, rowIndex);
                  console.log("Clicked!");
                },
              }}}
            />
          </ConfigProvider>
        </Col>
      </Row>

      <Drawer
        closeIcon={null}
        footer={null}
        width={"40%"}
        onClose={onDrawerClose}
        open={openDrawer}
      >
        <div className="my-drawer-container">
          <div className="my-drawer-header">
            <Space align="center">
              <h1>{innerName}</h1>
              <Tag
                bordered={false}
                color="rgba(238, 242, 247)"
                style={{
                  color: "rgba(106, 112, 129)",
                  padding: "0 14px",
                }}
              >
                Python
              </Tag>
            </Space>
            <CloseOutlined
              className="flex-center-xy  my-drawer-close-icon"
              onClick={onDrawerClose}
            />
          </div>

          <div className="my-drawer-top">
            <div className="my-drawer-top-item">
              <span className="my-drawer-top-item-label ">Name</span>
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
                  value={innerName}
                  onChange={onEditInnerName}
                  onBlur={innerNameBlur}
                  onPressEnter={innerNameBlur}
                />
              </ConfigProvider>
            </div>
            <div className="my-drawer-top-item">
              <span className="my-drawer-top-item-label ">Modified</span>
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
                  value={innerTime}
                  readOnly={true}
                
                />
                </ConfigProvider>
            </div>
          </div>
          <div className="my-drawer-content">
             <CodeMirror
              value={showContent()}
              theme="light"
              extensions={[python()]}
              onChange={editCode}
              className="custom-codemirror"
            />
          </div>
         
        </div>
      </Drawer>
    </>
  );
};

export default Page2;
