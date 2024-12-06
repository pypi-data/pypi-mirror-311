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
} from "@ant-design/icons";

import { useEffect, useState } from "react";

import MyRowPopover from "@/components/RowPopover";
import MySelectPopover from "@/components/SelectPopover";

import { addData2Share, getDatasets, getShare, getSharings, removeDataAccess } from "../../backend/networking";
import { useFetcher } from "react-router-dom";

const TableFooter = ({
  user = 'jcsiudhuewhduiwh',
  datasets =[],
  complete, 
}) => {
  return (
    <div className="my-table-custom-footer">
      <span className="my-table-custom-footer-label">
        <label>Shared With:</label> {user}
      </span>

      <MySelectPopover placement="leftTop" elements={datasets} complete={complete}>
        <Button color="default" variant="filled" icon={<PlusOutlined />}>
          Add new Button
        </Button>
      </MySelectPopover>
    </div>
  );
};

const Page5 = () => {

  const [counter, setCounter] = useState(0); 

  const [tableData, setTableData] = useState([
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
  ]);

  const saveEditPopoverContent = (index, value) => {
    tableData[index].value5 = value;
    setTableData([...tableData]);
  };

  const [shares, setShares] = useState([]); 
  const [datasets, setDatasets] = useState([]);

  const processSharings = (value)=> {
    setShares(value.sharings); 
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
      stats={{ cmu: 8, ppu: 0, mpp: "xxx AA" }}
      datasets={datasets}
      reload={reload}
      counter={counter}
    />
    }
  ):'');

  return (
    <>
      <Row justify="center" align="middle">
        <Col xs={22} sm={22} md={22} lg={22} xl={20} className="page-container">

          <div style={{height:'30px'}}></div> {/* Padding */}

          <Flex align="center" justify="space-between">
            <h1>Page 5</h1>
            <Button type="primary" shape="round" icon={<PlusCircleOutlined />}>
              Add new Button
            </Button>
          </Flex>

          <div style={{height:'20px'}}></div> {/* Padding */}

          {/*<Flex align="center" justify="space-between">
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
          </Flex>*/}

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
              /*shares.map((item, index)=> item.name.toLowerCase().includes(searchText.toLowerCase())?(<CustomTable 
                  mainData={item}
                  headerTitle={item.name}
                  stats={{ cmu: 8, ppu: 0, mpp: "xxx AA" }}
                  datasets={datasets}
                  reload={reload}
                  counter={counter}
                />):'')*/
                components
                  .sort((a, b) => a?.element?.name?.localeCompare(b?.element?.name))
                  .map((item) => item.widget)


            }

          </ConfigProvider>

          <div style={{height:'50px'}}></div>
        </Col>
      </Row>
    </>
  );
};


const CustomTable = ({ 
  mainData, 
  headerTitle = "Something displayed",
  headerAvatar = "W",
  avatarBgColor = "#f08e44",
  stats = { cmu: 8, ppu: 0, mpp: "xxx AA" }, 
  datasets = [],
  reload, 
  counter, 
}) => {
  const columns = [
    {
      title: "Data",
      dataIndex: "value1",
      key: "value1",
      render: (text) => (
        <Space size={"middle"}>
          <Avatar size={35} shape="square">
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
      title: "XXXXX",
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
          isOnlyShow={false}
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

  const [newMainData, setNewMainData] = useState(mainData); 

  const [dataIDs, setDataIDs] = useState(newMainData.data_shares.map((item,index)=> item.data_id)); 

  const getTableData = ()=>newMainData.data_shares.map((item, index)=> ({
    key: `${index}`,
    value1: item.name,
    value2: "Numpy",
    value3: item.shape,
    value4: item.size,
    value5: item.description
  }))


  const removeAt = (index)=>{
    const targetDataID = newMainData.data_shares[index].data_id; 
    const targetAccessKey = newMainData.access_key;
    const newList = newMainData.data_shares.filter((_, i) => i !== index)
    newMainData.data_shares = newList; 
    setNewMainData(newMainData); 
    setDataIDs(newList.map((item,index)=> item.data_id));
    setNewTableData(newList.map((item, index)=> ({
      key: item.data_id,
      value1: item.name,
      value2: "Numpy",
      value3: item.shape,
      value4: item.size,
      value5: item.description
    })));
    removeDataAccess(targetDataID, targetAccessKey).then((value)=> {
      reloadThis(); 
    })
  }


  const [newTableData, setNewTableData] = useState(getTableData());

  const processThis = (value)=>{
    console.log(value.sharing);
    setNewMainData(value.sharing); 
    setDataIDs(value.sharing.data_shares.map((item,index)=> item.data_id)); 
    setNewTableData(value.sharing.data_shares.map((item, index)=> ({
      key: `${index}`,
      value1: item.name,
      value2: "Numpy",
      value3: item.shape,
      value4: item.size,
      value5: item.description
    })));

  }

  const reloadThis = ()=>{
    getShare(newMainData.access_key).then(processThis); 
  }


  const complete = (item) => {
    setNewTableData((prev)=>{
      return [...prev, {
        key: `${prev.length}`,
        value1: item.name,
        value2: "Numpy",
        value3: item.shape,
        value4: item.size,
        value5: item.description
      }]
    });
    setDataIDs((prev)=> [...prev, item.data_id]);
    addData2Share(item.data_id, mainData.access_key).then((value)=>{
      reloadThis();
      reload(); 
    });
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
          <span>CMU: {stats.cmu}</span>
          <span>PPU: {stats.ppu}</span>
          <span>MPP: {stats.mpp}</span>
        </Space>
      </div>
      <Table
        dataSource={newTableData}
        columns={columns}
        rowClassName={() => "my-table-row-custom"}
        pagination={{ position: [] }}
        footer={() => <TableFooter user={mainData.to_user} datasets={datasets.filter((value)=>!dataIDs.includes(value.data_id))} 
        complete={complete}></TableFooter>}
        
      />
    </div>
  );
};


export default Page5;
