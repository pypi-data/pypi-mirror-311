import "./style.scss";
import "@/assets/styles/custom-table.scss";
import {
  Row,
  Col,
  Flex,
  Input,
  Button,
  Select,
  Table,
  ConfigProvider,
  Space,
  Avatar,
  Tag,
} from "antd";
import { SearchOutlined, PictureFilled, DownOutlined } from "@ant-design/icons";
import { useEffect, useState } from "react";

import MyRowPopover from "@/components/RowPopover";
import { checkPwd, getEnvironments, getRemoteEnv } from "../../backend/networking";
import { useNavigate } from "react-router-dom";
import { getPwd } from "../../backend/security";

// Images
import data_avatar from "@/assets/images/data_file.png";



const TableComponent = ({ data, columns, subData, addSubData }) => {

  /*const [tableData, setTableData] = useState([
    {
      key: "1",
      value1: "Sed ut perspiciatis",
      value2: "NNNPN",
      value3: "XXXXXXXXXXXXX",
      value4: "XXXXXXXXXXXXX",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
    {
      key: "2",
      value1: "Lorem Ipsum is simply dummy text of",
      value2: "NNNPN",
      value3: "XXXXXXXXXXXXX",
      value4: "XXXXXXXXXXXXX",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
  ]);*/

  const [tableData, setTableData] = useState([]);

  const processRemoteEnvs = (value)=>{
    const newData = value.env.data_shares.map((item, index)=>({
      key: `${index}`,
      value1: item.name,
      value2: "Numpy",
      value3: item.shape,
      value4: item.size,
      value5: item.description, 
    })); 
    //setTableData(newData); 
    addSubData(data.access_key, newData); 
  }

  const loadRemoteEnvs = async () => {
    getRemoteEnv(data.access_key).then(processRemoteEnvs)
  }

  useEffect(()=>{
    loadRemoteEnvs(); 
  },[])

  return (
    <ConfigProvider
      theme={{
        components: {
          Table: {
            headerBg: "transparent",
            headerColor: "rgba(106, 112, 129)",
            borderColor: "rgba(225, 228, 232)",
          },
        },
        token: {
          colorBgContainer: "transparent",
        },
      }}
    >
      <div className="my-table-custom" style={{borderRadius:'10px', overflow:'hidden'}}>
        <div className="my-table-custom-header">
          <Space size={"middle"}>
            <Avatar
              size={25}
              shape="square"
              style={{ backgroundColor: "#f08e44", fontSize: 14 }}
            >
              F
            </Avatar>
            <p className="text-line-1-ellipsis my-table-custom-header-title">
              {data.name}
            </p>
          </Space>
          <Space size={90} style={{ marginRight: 150 }}>
            {/*<span>ABC: 0</span>
            <span>EDF: 0</span>
            <span>GHI: XXX</span>*/}
            <span>Owner: {data.owner}</span>
          </Space>
        </div>
        <Table
          dataSource={subData[data.access_key]}
          columns={columns}
          rowClassName={() => "my-table-row-custom"}
          pagination={{ position: [] }}
        />
      </div>
    </ConfigProvider>
  );
};

const Page4 = () => {

  const navigate = useNavigate();

  useEffect(()=>{
    checkPwd(getPwd()).then((val)=>{
      if(val.match===false){
        navigate('/login'); 
      }
    })
  }, [])
  /*const [tableData, setTableData] = useState([
    {
      key: "1",
      value1: "Sed ut perspiciatis",
      value2: "NNNPN",
      value3: "XXXXXXXXXXXXX",
      value4: "XXXXXXXXXXXXX",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
    {
      key: "2",
      value1: "Lorem Ipsum is simply dummy text of",
      value2: "NNNPN",
      value3: "XXXXXXXXXXXXX",
      value4: "XXXXXXXXXXXXX",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
  ]);*/


  const [tableData, setTableData] = useState([]);


  const [subData, setSubData] = useState({
    untitle: null,
  }); 

  const addSubData = (key, value) => {
    setSubData((prev) => ({
      ...prev,
      [key]: value
    }));
  }

  const columns = [
    {
      title: "DATA",
      dataIndex: "value1",
      key: "value1",
      render: (text) => (
        <Space size={"middle"}>
          <Avatar size={35} shape="square"
            src={data_avatar}
          >
            
          </Avatar>
          <p
            className="text-line-1-ellipsis"
            style={{ width: 300, margin: 0, fontWeight: 500 }}
          >
            {text}
          </p>
        </Space>
      ),
      width: 380,
    },
    {
      title: "FORMAT",
      dataIndex: "value2",
      key: "value2",
      render: (text) => (
        <Tag
          bordered={false}
          color="#d1dcf7"
          className="my-tag-custom"
          style={{ color: "#3f74f6" }}
        >
          {text}
        </Tag>
      ),
    },
    {
      title: "SHAPE",
      dataIndex: "value3",
      key: "value3",
    },
    {
      title: "SIZE",
      dataIndex: "value4",
      key: "value4",
    },
    {
      title: "DESCRIPTION",
      dataIndex: "value5",
      key: "value5",
      width: 280,
      render: (text) => (
        <>
          <Space size={"middle"}>
            <p
              className="text-line-1-ellipsis"
              style={{ margin: 0, width: 280 }}
            >
              {text}
            </p>
            <MyRowPopover showText={text} isOnlyShow={true}>
              <Button
                style={{ background: "#b6bbc6", border:'none' }}
                size="small"
                icon={<DownOutlined style={{ fontSize: 12, color: "#fff" }} />}
              ></Button>
            </MyRowPopover>
          </Space>
        </>
      ),
    },
  ];

  const [environments, setEnvironments] = useState([])

  const [sortOrder, setSortOrder] = useState("1"); // Add this new state

  const handleSort = async (value) => {
    setSortOrder(value);
    const sortedEnvs = [...environments].sort((a, b) => {
      if (value === "1") {
        return a.name.localeCompare(b.name);
      } else {
        return b.name.localeCompare(a.name);
      }
    });
    setEnvironments(sortedEnvs);
  };

  const processEnvironments = (value)=>{
    setEnvironments(value.envs);
    console.log('here')
    console.log(value); 
  }

  const loadEnvironments = async () => {
    getEnvironments().then(processEnvironments); 
  }

  useEffect(()=>{
    loadEnvironments(); 
  },[])

  return (
    <>
      <Row justify="center" align="middle">
        <Col xs={22} sm={22} md={22} lg={22} xl={20} className="page-container">

          <div style={{height:'30px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <h1>Shared with me</h1>
          </Flex>

          <div style={{height:'20px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <Select
              value={sortOrder}
              style={{ width: 150 }}
              options={[
                { value: "1", label: "A - Z" },
                { value: "2", label: "Z - A" },
              ]}
              onChange={(value)=>handleSort(value)}
            />

            <Input
              placeholder="Search"
              style={{ width: 200 }}
              prefix={<SearchOutlined style={{ color: "rgba(0,0,0,0.45)" }} />}
            />
          </Flex>

          <div style={{height:'10px'}}></div> {/* Padding */}

          {
            environments.map((item, index) => (
              <TableComponent 
                key={index}
                data={item}
                columns={columns}
                subData={subData}
                addSubData={addSubData}
              />
            ))
          }

          <div style={{height:'50px'}}></div>

        </Col>
      </Row>
    </>
  );
};

export default Page4;
