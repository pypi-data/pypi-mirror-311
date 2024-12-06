import {
    Row,
    Col,
    Flex,
    Button,
    Input,
    Table,
    Space,
    Avatar,
    Drawer,
    Form,
  } from "antd";
import { CloseOutlined, PictureFilled } from "@ant-design/icons";
import { getDatasets, share } from "../backend/networking";
import { useEffect, useState } from "react";


const CustomDrawer = ({ open, onClose, reload=null}) => {


    const [dataSource, setDataSource] = useState([
        {
          id: 1,
          value1: "Lorem Ipsum",
          value2: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry.`,
        },
        {
          id: 2,
          value1: "Lorem Ipsum",
          value2: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry.`,
        },
        {
          id: 3,
          value1: "Lorem Ipsum",
          value2: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry.`,
        },
        {
          id: 4,
          value1: "Lorem Ipsum",
          value2: `Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry.`,
        },
      ]);

    const [datasets, setDatasets] = useState([]); 

    const [environmentName, setEnvironmentName] = useState("");

    const [ipAddress, setIpAddress] = useState("");

    const [selectedIds, setSelectedIds] = useState([]);

    const columns = [
        {
          title: "DATA",
          dataIndex: "value1",
          key: "value1",
          render: (text, item, index) => (
            <Space size={"middle"}>
              <Avatar size={40} shape="square">
                <PictureFilled style={{ fontSize: 20 }} />
              </Avatar>
              <div className="my-table-row-title">
                <p className="text-line-1-ellipsis">{text}</p>
                <p className="my-row-attr">
                  <span>{datasets[index].size}</span>
                  <span>{datasets[index].shape}</span>
                  <span>NumPy</span>
                </p>
              </div>
            </Space>
          ),
        },
        {
          title: "DESCRIPTION",
          dataIndex: "value2",
          key: "value2",
          width: "50%",
          render: (text) => (
            <p className="text-line-2-ellipsis" style={{ margin: 0 }}>
              {text}
            </p>
          ),
        },
      ];

    const processData = (value)=>{
        setDatasets(value.datasets); 
        setDataSource(value.datasets.map((item, index)=> ({
            id: item.data_id,
            value1: item.name,
            value2: item.description
        })))
    }
    const loadData = async ()=> {
        getDatasets().then(processData); 
    }

    useEffect(()=>{
        loadData(); 
    },[])

    const rowSelection = {
        selectedRowKeys: selectedIds,
        onChange: (selectedRowKeys, selectedRows) => {
            console.log(
                `selectedRowKeys: ${selectedRowKeys}`,
                "selectedRows: ",
                selectedRows
            );
            setSelectedIds(selectedRowKeys);
        },
        getCheckboxProps: (record) => ({
            disabled: record.name === "Disabled User",
            // Column configuration not to be checked
            name: record.name,
        }),
    };



    const onConfirmed = (value) => {
      if (value.status==1){
        setConnErr(''); 
        onClose(); 
        reload!==null?reload():null; 
        setSelectedIds([]);
        setEnvironmentName('');
        setIpAddress(''); 
        return; 
      }
      setConnErr('Connection Error')
    }

    const [connErr, setConnErr] = useState(''); 

    const confirmShare = async ()=>{
      if(ipAddress==='' || environmentName===''){
        console.log('Nothing');
        return; 
      }
        share(ipAddress, environmentName, selectedIds).then(onConfirmed).catch((e)=>{
          setConnErr('Connection Error')
        }); 
    }

return (
    <Drawer
    closeIcon={null}
    footer={null}
    width={"100%"}
    onClose={onClose}
    open={open}
    title={
        <Space align="center" size="middle">
        <Avatar size={33} shape="square">
            <PictureFilled style={{ fontSize: 20 }} />
        </Avatar>
        <span style={{ borderLeft: "1px solid #e8e8e8", paddingLeft: "30px" }}>
        Create new environment
        </span>
        </Space>
    }
    extra={
        <CloseOutlined
        style={{
            cursor: "pointer",
            marginRight: "10px",
            borderRadius: "50%",
            border: "1px solid #999",
            padding: "8px",
            color: "#999",
        }}
        onClick={onClose}
        />
    }
    >
    <Row justify="center" align="middle">
        <Col
        xs={22}
        sm={22}
        md={20}
        lg={16}
        xl={12}
        className="page-container"
        >
        <h1 style={{ marginBottom: "60px" }}>Create new environment</h1>

        <Form layout="vertical">
            <Form.Item
            label="Title of environment"
            name="value1"
            rules={[
                {
                required: true,
                message: "Please input!",
                },
            ]}
            >
            <Input 
                placeholder="Name of the environment" 
                value={environmentName}
                onChange={(e) => setEnvironmentName(e.target.value)}
            />
            </Form.Item>
            <Form.Item label="Share with">
            <Input 
                placeholder="IP Address" 
                value={ipAddress}
                onChange={(e) => setIpAddress(e.target.value)}
            />
            </Form.Item>
            <Form.Item
            label="Select Data"
            name="table"
            rules={[
                {
                required: true,
                message: connErr,
                },
            ]}
            >
            <Table
                className="my-table"
                dataSource={dataSource}
                columns={columns}
                rowKey={"id"}
                rowSelection={{
                    type: "checkbox",
                    ...rowSelection,
                  }}
                pagination={false}
            />
            </Form.Item>
            <Form.Item>
            <Flex justify="space-between" align="center">
                <span style={{ color: "#6a7081", fontWeight: 500 }}>
                Check Documentation
                </span>

                <Button color="default" variant="solid" htmlType="submit" onClick={confirmShare}>
                Confirm
                </Button>
            </Flex>
            </Form.Item>
        </Form>
        </Col>
    </Row>
    </Drawer>
);
};

export  {CustomDrawer, }; 