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
  Tag,
} from "antd";
import {
  PlusCircleOutlined,
  SearchOutlined,
  PictureFilled,
  RightOutlined,
  CheckOutlined,
  CloseOutlined,
} from "@ant-design/icons";
import EllipsisSvg from "@/assets/svg/ellipsis.svg";
import EditSvg from "@/assets/svg/edit.svg";

import { useEffect, useState } from "react";

import MyRowPopover from "@/components/RowPopover";

import {checkPwd, describeData, getDatasets, handleDataFileUpload, renameData} from '../../backend/networking';
import { useNavigate } from "react-router-dom";
import { getPwd } from "../../backend/security";

// Images
import data_avatar from "@/assets/images/data_file.png";


const Page3 = () => {

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
      value1: "Lorem Ipsum is simply dummy text of",
      value2: "1",
      value3: "XXXXXXXXXXXXX",
      value4: "XXXXXXXXXXXXX",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
    {
      key: "2",
      value1: "Lorem Ipsum is simply dummy text of",
      value2: "2",
      value3: "XXXXXXXXXXXXX",
      value4: "XXXXXXXXXXXXX",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
  ]);*/

  const [tableData, setTableData] = useState([]);

  const [editRow, setEditRow] = useState({
    value: "",
    index: "",
  });

  const [searchText, setSearchText] = useState("");

  const [sortOrder, setSortOrder] = useState("1");

  const doRenameData = (dataName, dataID) => {
    renameData(dataName, dataID).then((value)=>{
      loadData(); 
    })
  }

  const RowEditColums = (text, item, index) => {
    const saveEditRow = (index, value) => {
      doRenameData(value, tableData[index].key); 
      tableData[index].value1 = value;
      setTableData([...tableData]);
      console.log(index, value);
      
      setEditRow({
        index: "",
        value: "",
      });
      
    }

    return (
      <>
        <Space size={"middle"}>
          <Avatar size={35} shape="square" src={data_avatar}>
          </Avatar>
          {index === editRow.index ? (
            <>
              <Input
                value={editRow.value}
                //value={inputText}
                suffix={
                  <CheckOutlined
                    style={{
                      paddingLeft: 5,
                      color: "#57a2ff",
                    }}
                    onClick={() => {
                      console.log('ok')
                      saveEditRow(index, editRow.value);
                    }}
                  />
                }
                allowClear
                style={{ width: 240 }}
                onBlur={() => {
                  saveEditRow(index, editRow.value);
                }}
                onChange={(e) => {
                  setEditRow({
                    index,
                    value: e.target.value,
                  });
                }}
              />
            </>
          ) : (
            <>
              <p
                className="text-line-1-ellipsis"
                style={{ width: 200, margin: 0 }}
              >
                {text}
                
              </p>
              <img
                src={EditSvg}
                alt="edit"
                style={{ cursor: "pointer", marginLeft: 1 }}
                onClick={() => {
                  setEditRow({
                    index,
                    value: text,
                  });
                }}
              />
            </>
          )}
        </Space>
      </>
    );
  };

  const saveEditPopoverContent = (index, value) => {
    tableData[index].value5 = value;
    describeData(value, tableData[index].key).then((value)=>{
      loadData(); 
    });
    setTableData([...tableData]);
  };

  const columns = [
    {
      title: "DATA",
      dataIndex: "value1",
      key: "value1",
      render: (text, item, index) => RowEditColums(text, item, index),
      width: 380,
    },
    {
      title: "FORMAT",
      dataIndex: "value2",
      key: "value2",
      render: () => (
        <Tag
          bordered={false}
          color="#d1dcf7"
          className="my-tag-custom"
          style={{ color: "#3f74f6" }}
        >
          Label
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
      title: "Description",
      dataIndex: "",
      key: "",
      width: 100,
      render: (text, item, index) => (
        <MyRowPopover
          showText={item.value5}
          item={item}
          index={index}
          isOnlyShow={false}
          saveCallback={saveEditPopoverContent}
        >
          <Tag
            bordered={false}
            color="#d4e7fe"
            className="my-tag-custom"
            style={{ color: "#57a1fe", cursor: "pointer" }}
          >
            Note
            <RightOutlined style={{ marginLeft: 15 }} />
          </Tag>
        </MyRowPopover>
      ),
    },
    {
      title: "",
      dataIndex: "",
      key: "",
      width: 100,
      align: "center",
      render: () => (
        <button className='button-remove-data'>
          <CloseOutlined className='icon' />
        </button>
      ),
    },
  ];


  //const [mainData, setMainData] = useState([])


  const processData = (value)=>{
    var newData = value.datasets.map((dataset)=> ({
      key: dataset.data_id,
        value1: dataset.name,
        value3: dataset.shape,
        value4: dataset.size,
        value5: dataset.description,
    }));
    //setMainData(value.datasets); 
    setTableData([...newData]);
  }

  const loadData = async ()=> {
    getDatasets().then(processData); 
  }

  useEffect(()=>{
    loadData();
  }, [])



  const uploadFunction = async (event)=>{
    handleDataFileUpload(event).then((value)=>{
      loadData(); 
    })
  } 

  const sortData = (value) => {
    setSortOrder(value);
    setTableData(prev => {
      console.log('Before sort length:', prev.length);
      const newData = [...prev].sort((a, b) => {
        if (value === "1") {
          return a.value1.localeCompare(b.value1);
        }
        return b.value1.localeCompare(a.value1);
      });
      console.log('After sort length:', newData.length);
      return newData;
    });
  };

  return (
    <>
      <Row justify="center" align="middle">
        <Col xs={22} sm={22} md={22} lg={22} xl={20} className="page-container">

          <div style={{height:'30px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <h1>My data</h1>
            <Button type="primary" shape="round" icon={<PlusCircleOutlined />}>
    
              <label htmlFor="file-upload" style={{ cursor: "pointer" }}>
                Upload Numpy File
              </label>

              <input
                type="file"
                accept=".npy"
                style={{ display: "none" }}
                onInput={uploadFunction
                }
                id="file-upload"
              />
            </Button>
          </Flex>

          <div style={{height:'20px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <Select
              value={sortOrder}
              onChange={(value) => {
                sortData(value);
              }}
              style={{ width: 150 }}
              options={[
                { value: "1", label: "A - Z" },
                { value: "2", label: "Z - A" },
              ]}
            />

            <Input
              placeholder="Search project"
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
              dataSource={tableData.filter((value)=>value.value1.toLowerCase().includes(searchText.toLowerCase()))}
              columns={columns}
              style={{
                marginTop: 30,
              }}
              rowClassName={() => "my-table-row-custom"}
              pagination={{ position: [] }}
            />
          </ConfigProvider>
        </Col>
      </Row>
    </>
  );
};

export default Page3;
