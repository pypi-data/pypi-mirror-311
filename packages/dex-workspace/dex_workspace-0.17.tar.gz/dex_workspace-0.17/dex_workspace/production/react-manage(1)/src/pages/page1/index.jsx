import { useEffect, useState } from "react";
import "./style.scss";
import {
  Row,
  Col,
  Flex,
  Button,
  Input,
  Segmented,
  Table,
  Tag,
  ConfigProvider,
  Space,
  Avatar,
  Checkbox,
} from "antd";
import {
  PlusCircleOutlined,
  SearchOutlined,
  PictureFilled,
  RightOutlined,
  MoreOutlined
} from "@ant-design/icons";
import EllipsisSvg from "@/assets/svg/ellipsis.svg";

import { useNavigate } from "react-router-dom";

import {checkPwd, deleteProjects, getProjects, newProject, } from '../../backend/networking';
import { getPwd } from "../../backend/security";

// Images
import project_logo from "@/assets/images/dex.png";


/* Status filter */
const SegmentedItemLabel = (label, count) => {
  return (
    <div style={{ color: "#727888" }}>
      <span style={{ color: "#000", paddingRight: 5 }}>{label}</span> {count}
    </div>
  );
};/* Status filter */



const Page1 = () => {
  const navigate = useNavigate();

  

  /*const [tableData, setTableData] = useState([
    {
      key: "1",
      value1: "Lorem Ipsum is simply dummy text of",
      value2: 1,
      value3: "Lorem Ipsum",
      value4: "Text",
      value5: "Lorem Ipsum",
    },
    {
      key: "2",
      value1:
        "Lorem Ipsum is simply dummy text of the Lorem Ipsum is simply dummy text of the",
      value2: 2,
      value3: "Lorem Ipsum",
      value4: "Text",
      value5: "Lorem Ipsum",
    },
  ]);*/

  const [tableData, setTableData] = useState([]);

  const [selectedIDs, setSelectedIDs] = useState([]); 

  const onProjChecked = (event, item)=>{
    console.log(event.target.value);
    if(event.target.value){
      setSelectedIDs((prev)=> prev.filter((e)=> e!=item.key)); 
    }else{
      setSelectedIDs((prev)=>[...prev, item.key]); 
    }
    console.log(selectedIDs); 
  }

  const columns = [
    {
      title:'',
      width: 10,
      align: 'center',
      render: (text, item, index) => (
        <div style={{ marginLeft:'5px'}}> 
        <Checkbox 
            value={selectedIDs.includes(item.key)} 
            onChange={ (e)=>{onProjChecked(e, item)} } 
        />
        </div>
      ),
    },
    {
      title: "PROJECT",
      dataIndex: "value1",
      key: "value1",
      render: (text) => (
        <Space size={"middle"}>
          {/* Table: Row - Image */}
          <Avatar size={35} shape="square" style={{overflow:'hidden', padding:'0'}}

          src={project_logo}
          >
          
          </Avatar>
          <div className="my-row-title">
            <p className="text-line-1-ellipsis">{text}</p>
            <span style={{fontSize:'.9em'}}>Federated Learning</span>
          </div>
        </Space>
      ),
      width: 280,
    },
    {
      title: "STATUS",
      dataIndex: "value2",
      key: "value2",
      render: (text) => {
        switch (text + "") {
          case "1":
            return (
              <Tag
                bordered={false}
                color="#d2f5de"
                className="my-tag-custom"
                style={{ color: "#1dcf5a" }}
              >
                Running
              </Tag>
            );
          case "2":
            return (
              <Tag
                bordered={false}
                color="#fff2d1"
                className="my-tag-custom"
                style={{ color: "#ffbe17" }}
              >
                Idle
              </Tag>
            );
          default:
            break;
        }
      },
    },
    {
      title: "MAIN SCRIPT",
      dataIndex: "value3",
      key: "value3",
    },
    {
      title: "DATA",
      dataIndex: "value4",
      key: "value4",
    },
    {
      title: "CREATED AT",
      dataIndex: "value5",
      key: "value5",
    },
    {
      title: "",
      dataIndex: "",
      key: "",
      width: 100,
      align: "center",
      render: (text, item, index) => (
        <button
          className="go_to_project"
          src={EllipsisSvg}
          alt=""
          style={{
            cursor: "pointer",
          }}
          onClick={() => {
            navigate(`/page-11?key=${item.key}`);
          }}
        >
          <RightOutlined className="icon"/>
        </button>
      ),
    },
    /*
    {
      title: "",
      dataIndex: "",
      key: "",
      width: 50,
      align: "center",
      render: (text, item, index) => (
        <button
          className="go_to_project"
          src={EllipsisSvg}
          alt=""
          style={{
            cursor: "pointer",
          }}
          onClick={() => {
            navigate(`/page-11?key=${item.key}`);
          }}
        >
          <MoreOutlined className="icon"/>
        </button>
      ),
    },*/
  ];

  const SegmentedOptions = [
    {
      label: SegmentedItemLabel("All", tableData.length),
      value: "0",
    },
    {
      label: SegmentedItemLabel("Running", tableData.filter((e)=>e.value2==1).length),
      value: "1",
    },
    {
      label: SegmentedItemLabel("Idle",  tableData.filter((e)=>e.value2==2).length),
      value: "2",
    },
  ];
  const [SegmentedVal, setSegmentedVal] = useState("0");
  const [searchText, setSearchText] = useState("");

  const processProjects = (value)=> {
    const updatedProjects = value.projects.map(project => ({
      key: project.project_id,
      value1: project.name,
      value2: project.running?1:2,
      value3: project.script_name!==null ? project.script_name : '-',
      value4: project.num_envs,
      value5: project.update_time,
    }));
    setTableData(updatedProjects);
  }

  const loadProjects = async () =>  {
    getProjects().then(processProjects)
  }

  const filteredTable = ()=>{
    return tableData.filter((value)=>value.value1.toLowerCase().includes(searchText.toLowerCase())); 
  }

  const categorizeTable = ()=>{
    if(SegmentedVal=='0'){
      return filteredTable();
    }else if(SegmentedVal=='1'){
      return filteredTable().filter((e)=>e.value2==1);
    }else{
      return filteredTable().filter((e)=>e.value2==2); 
    }
  }

  const removeProjects = ()=>{
    deleteProjects(selectedIDs).then((v)=>{
      loadProjects(); 
    }); 
    setTableData(
      (prev)=>prev.filter((e)=>selectedIDs.includes(e.key)==false)
    ); 
    setSelectedIDs([]);
  }

  useEffect(()=>{
    loadProjects();
  }, [])

  return (
    <>
      <Row justify="center" align="middle">
        <Col xs={22} sm={22} md={22} lg={22} xl={20} className="page-container">

          <div style={{height:'30px'}}></div> {/* Padding */}


            <Flex align="center" justify="space-between">

              <h1>Project management</h1>

              <Button 
                style={{
                  backgroundColor:'#497BFD',
                  border: 'none',
                  padding:"20px 20px",
                  color: '#fff'
                }} shape="round" icon={<PlusCircleOutlined />}

                className = 'add_new_button'
                onClick={()=>{
                  newProject().then((value)=>{
                    loadProjects(); 
                  })
                }}
              >
                Create new project
              </Button>

            </Flex>

            <div style={{height:'20px'}}></div> {/* Padding */}
            
            <Flex align="center" justify="space-between">
              <Segmented
                options={SegmentedOptions}
                style={{
                  backgroundColor: "#EAEDF1",
                  padding: "2.5px",
                }}
                value={SegmentedVal}
                onChange={(value) => {
                  console.log(value); 
                  setSegmentedVal(value);
                }}
              />

              <Input
                placeholder="Search"
                style={{ width: 200 }}
                prefix={<SearchOutlined style={{ color: "rgba(0,0,0,0.45)" }} />}
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
              />
            </Flex>

            {/* Project Table { */}
            <ConfigProvider
              theme={{
                components: {
                  Table: {
                    headerBg: "#EDEFF3", /* #EDEFF3 */
                    headerColor: "rgba(106, 112, 129)",
                    borderColor: "rgba(225, 228, 232)",

                  },
                },
              }}
            >
              <Table
                dataSource={categorizeTable()}
                columns={columns}
                style={{
                  marginTop: 30,
                }}
                rowClassName={() => "my-table-row-custom"}
                pagination={{ position: [] }}
                onRow={(record, rowIndex) => {
                  return {
                    onClick: () => {
                      console.log("Clicked!", rowIndex); // Click: Go to project
                   
                    },
                }}}
              />
              <div className='ctn-remove-project'>
               
                <button className={`button ${selectedIDs.length>0?'active':''}`} onClick={removeProjects}>
                  {`Remove (${selectedIDs.length})`}
                </button>
              </div>
            </ConfigProvider>{/* Project Table } */}
        </Col>
      </Row>
    </>
  );
};

export default Page1;
