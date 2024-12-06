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
import {
  SearchOutlined,
  PictureFilled,
  CloseOutlined,
  PlusCircleOutlined,
  RightOutlined,
  PlusOutlined,
  DeleteOutlined
} from "@ant-design/icons";

import { useEffect, useState } from "react";

import MyRowPopover from "@/components/RowPopover";
import MySelectPopover from "@/components/SelectPopover";

import { addData2Share, checkPwd, getDatasets, getShare, getSharings, removeDataAccess, removeSharing, share } from "../../backend/networking";
import { useFetcher, useNavigate } from "react-router-dom";
import { CustomDrawer } from "../../components/drawers";
import { getPwd } from "../../backend/security";

// Images
import data_avatar from "@/assets/images/data_file.png";



const TableFooter = ({
  user = 'jcsiudhuewhduiwh',
  datasets =[],
  complete, 
  onRemove, 
}) => {
  return (
    <div className="my-table-custom-footer">
      <span className="my-table-custom-footer-label">
        <label>Shared With:</label> {user}
      </span>

      <MySelectPopover placement="leftTop" elements={datasets} complete={complete}>
        <Button color="default" variant="filled" icon={<PlusOutlined />}>
          Add new data
        </Button>
      </MySelectPopover>

      <Button type="primary" icon={<DeleteOutlined />} className="button-remove-section"
        style={{marginLeft:'10px', color:'#FF3162', backgroundColor:'rgb(255, 49, 98, .1)', border:'none'}}
        onClick={onRemove}
        >
          Remove
        </Button>

        

    </div>
  );
};

const Page5_1 = () => {

  const navigate = useNavigate();

  useEffect(()=>{
    checkPwd(getPwd()).then((val)=>{
      if(val.match===false){
        navigate('/login'); 
      }
    })
  }, [])

  const [counter, setCounter] = useState(0); 

  /*const [tableData, setTableData] = useState([
    {
      key: "1",
      value1: "Sed ut perspiciatis",
      value2: "NNNPN",
      value3: "XXXXXXX",
      value4: "50A",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
    {
      key: "2",
      value1: "omnis iste natus er",
      value2: "NNNPN",
      value3: "XXXXXXX",
      value4: "50A",
      value5: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make`,
    },
  ]);*/

  const [tableData, setTableData] = useState([]);


  const saveEditPopoverContent = (index, value) => {
    tableData[index].value5 = value;
    setTableData([...tableData]);
  };

  const [shares, setShares] = useState([]); 
  const [datasets, setDatasets] = useState([]);

  const processSharings = (value)=> {
    setShares(value.sharings); 
    //setShares(addDataIDs); 
  }

  const loadSharings = ()=>{
    getSharings().then(processSharings);
  }

  const processData = (value)=>{
    setDatasets(value.datasets);
  }

  const loadData = ()=>{
    getDatasets().then(processData); 
  }

  const reload = async ()=>{
    loadSharings();
    loadData(); 
  }

  useEffect(()=>{
    loadSharings();
    loadData();
  }, [])

  const [searchText, setSearchText] = useState("");

  const [sortOrder, setSortOrder] = useState("1"); 

  const components =  shares.map((item, index)=> item.name.toLowerCase().includes(searchText.toLowerCase())?(
    {
      element: item, 
      widget: <CustomTable 
      mainData={item}
      headerTitle={item.name}
      stats={{ cpu: 8, gpu: 0, mem: "xxx AA" }}
      datasets={datasets}
      reload={reload}
      tableIndex={index}
      allData={shares}
      setAllData={setShares}
    />
    }
  ):'');

  const [openDrawer, setOpenDrawer] = useState(false);

  const showDrawer = () => {
    setOpenDrawer(true);
  };

  const onDrawerClose = () => {
    setOpenDrawer(false);
  };

  return (
    <>
      <Row justify="center" align="middle">
        <Col xs={22} sm={22} md={22} lg={22} xl={20} className="page-container">

          <div style={{height:'30px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <h1>Sharig with others</h1>
            <Button
              type="primary"
              shape="round"
              icon={<PlusCircleOutlined />}
              onClick={showDrawer}
            >
              Invite collabortor
            </Button>
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
              onChange={(value)=>{
                setSortOrder(value);
              }}
            />

            <Input
              placeholder="Search"
              style={{ width: 200 }}
              prefix={<SearchOutlined style={{ color: "rgba(0,0,0,0.45)" }} />}
              onChange={(e) => setSearchText(e.target.value)}
            />
          </Flex>

          <div style={{height:'10px'}}></div> {/* Padding */}

          <ConfigProvider
            theme={{
              components: {
                Table: {
                  headerBg: "transparent",
                  headerColor: "rgba(106, 112, 129)",
                  borderColor: "rgba(225, 228, 232)",
                  footerBg: "transparent",
                  borderRadius: 10,
                },
              },
              token: {
                colorBgContainer: "transparent",
              },
            }}
          >
            
            {
                components
                  .sort((a, b) => sortOrder==="1"?a?.element?.name?.localeCompare(b?.element?.name)
                                :b?.element?.name?.localeCompare(a?.element?.name))
                  .map((item) => item.widget)

            }

          </ConfigProvider>

          <div style={{height:'50px'}}></div>
        </Col>
      </Row>
      <CustomDrawer 
        open={openDrawer} 
        onClose={onDrawerClose}
        reload={reload}
      />
    </>
  );
};


const CustomTable = ({ 
  mainData, 
  headerTitle = "Something displayed",
  headerAvatar = "W",
  avatarBgColor = "#f08e44",
  stats = { cpu: 8, gpu: 0, mem: "xxx AA" }, 
  datasets = [],
  reload, 
  tableIndex, 
  allData, 
  setAllData, 
}) => {
  const columns = [
    {
      title: "Data",
      dataIndex: "value1",
      key: "value1",
      render: (text) => (
        <Space size={"middle"}>
          <Avatar size={35} shape="square" 
            src={data_avatar}>
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
      render: (text, item, index) => (
        <MyRowPopover
          showText={item.value5}
          item={item}
          index={index}
          isOnlyShow={true}
        >
          <Tag
            bordered={false}
            color="#d4e7fe"
            className="my-tag-custom"
            style={{ color: "#57a1fe", cursor: "pointer" }}
            onClick={() => {}}
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
      render: (text, item, index) => (
        <CloseOutlined style={{ cursor: "pointer", color: "#aaaeb8" }} onClick={()=>{removeAt(index)}}/>
      ),
    },
  ];


  console.log(allData);


  const dataIDs = allData[tableIndex].data_shares.map((item)=> item.data_id); 

  var newTableData = allData[tableIndex].data_shares.map((item, index)=> ({
    key: `${index}`,
    value1: item.name,
    value2: "Numpy",
    value3: item.shape,
    value4: item.size,
    value5: item.description
  })); 

  const removeAt = (index)=>{
    console.log(index);
    removeDataAccess(
      allData[tableIndex].data_shares[index].data_id, 
      allData[tableIndex].access_key
    ).then((value)=>{
      reload(); 
    });
    setAllData((prev)=> {
      var newData = [...prev];
      newData[tableIndex].data_shares = [...newData[tableIndex].data_shares].filter((value, idx)=> idx!=index)
      return newData; 
    }); 
  }


  const complete = (item) => {
    console.log(item);
    console.log(allData);
    setAllData((prev)=>{
      var newData = [...prev];
      var newShare = {
        access_key: allData[tableIndex].access_key, 
        bytes_size: item.bytes_size, 
        data_id: item.data_id, 
        description: item.description, 
        name: item.name,
        shape: item.shape, 
        size: item.size, 
      };
      newData[tableIndex].data_shares = [...newData[tableIndex].data_shares, newShare]; 
      return newData;
    }); 
    addData2Share(item.data_id, allData[tableIndex].access_key).then((value)=>{
      reload(); 
    }); 
  } 

  const onRemoveSetData = (prev)=>{
    var newData = [...prev].filter((item, idx)=> idx!=tableIndex); 
    return newData; 
  }
  
  const onRemove = ()=> {
    removeSharing(allData[tableIndex].access_key).then((value)=>{
      reload(); 
    }); 
    setAllData(onRemoveSetData); 
  }

  return (
    <div className="my-table-custom" style={{borderRadius:'10px'}}>
      <div className="my-table-custom-header">
        <Space size={"middle"}>
          <Avatar
            size={25}
            shape="square"
            style={{ backgroundColor: avatarBgColor, fontSize: 14 }}
          >
            {headerAvatar}
          </Avatar>
          <p className="text-line-1-ellipsis my-table-custom-header-title">
            {headerTitle}
          </p>
        </Space>
        <Space size={90} style={{ marginRight: 150 }}>
          {/*<span>CPU: {stats.cpu}</span>
          <span>GPU: {stats.gpu}</span>
          <span>Memory: {stats.mem}</span>*/}
        </Space>
      </div>
      <Table
        dataSource={newTableData}
        columns={columns}
        rowClassName={() => "my-table-row-custom"}
        pagination={{ position: [] }}
        footer={() => <TableFooter 
          user={allData[tableIndex].to_user} 
          datasets={datasets.filter((value)=>!dataIDs.includes(value.data_id))} 
        complete={complete}
        onRemove={onRemove}
        
        ></TableFooter>}
        
      />
    </div>
  );
};


export default Page5_1;
