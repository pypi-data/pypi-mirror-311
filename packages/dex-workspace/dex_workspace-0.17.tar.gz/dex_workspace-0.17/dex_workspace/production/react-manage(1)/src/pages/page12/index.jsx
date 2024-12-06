import { useEffect, useState } from "react";
import "./style.scss";
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
import { CustomDrawer } from "../../components/drawers";
import { useNavigate } from "react-router-dom";
import { checkPwd } from "../../backend/networking";
import { getPwd } from "../../backend/security";

const rowSelection = {
  onChange: (selectedRowKeys, selectedRows) => {
    console.log(
      `selectedRowKeys: ${selectedRowKeys}`,
      "selectedRows: ",
      selectedRows
    );
  },
  getCheckboxProps: (record) => ({
    disabled: record.name === "Disabled User",
    // Column configuration not to be checked
    name: record.name,
  }),
};

const Page12 = () => {

  const navigate = useNavigate();

  useEffect(()=>{
    checkPwd(getPwd()).then((val)=>{
      if(val.match===false){
        navigate('/login'); 
      }
    })
  }, [])

  const [openDrawer, setOpenDrawer] = useState(false);
  const showDrawer = () => {
    setOpenDrawer(true);
  };
  const onDrawerClose = () => {
    setOpenDrawer(false);
  };


  const columns = [
    {
      title: "Dolor",
      dataIndex: "value1",
      key: "value1",
      render: (text) => (
        <Space size={"middle"}>
          <Avatar size={40} shape="square">
            <PictureFilled style={{ fontSize: 20 }} />
          </Avatar>
          <div className="my-table-row-title">
            <p className="text-line-1-ellipsis">{text}</p>
            <p className="my-row-attr">
              <span>25 XXXX</span>
              <span>dolorem</span>
              <span>adipisci</span>
            </p>
          </div>
        </Space>
      ),
    },
    {
      title: "consectetur",
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

  const [form] = Form.useForm();

  return (
    <>
      <Button type="primary" onClick={showDrawer}>
        Open
      </Button>
      <CustomDrawer 
        open={openDrawer} 
        onClose={onDrawerClose}// Pass dataSource as a prop
      />
    </>
  );
};
export default Page12;
