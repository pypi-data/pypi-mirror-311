import { SearchOutlined, DownOutlined, SmileOutlined } from "@ant-design/icons";
import { Layout, Dropdown, Avatar, Popover, Input } from "antd";
const { Header } = Layout;
import reactLogo from "@/assets/svg/react.svg";
import ChineseKnot from "@/assets/svg/Chinese-knot.svg";
import message from "@/assets/svg/message.svg";

import {appIP} from '../backend/otherInfo';

// Images
import logo from "@/assets/images/logo.png";

const items = [
  {
    key: "1",
    label: (
      <a
        target="_blank"
        rel="noopener noreferrer"
        //href="https://ant-design.antgroup.com"
      >
        Collaborator Endpoint
      </a>
    ),
  },
  {
    key: "2",
    label: (
      <a
        target="_blank"
        rel="noopener noreferrer"
        href="https://www.aliyun.com"
      >
        {`${appIP}:5678`}
      </a>
    ),
    icon: <SmileOutlined />,
    disabled: true,
  },
  {
    key: "4",
    danger: true,
    label: "User Information",
  },
];

const MyHeader = () => {
  return (
    <>
      <Header className="layout-header">
        <div className="logo" style={{height:'70%'}}>
          <img src={logo} alt="logo"  style={{height:'100%'}} />
        </div>
        <Popover
          placement="bottom"
          trigger="click"
        >
          <div className="search-box">
            <SearchOutlined style={{ marginRight: "8px" }} />
            Search ({" "}
            <img
              src={ChineseKnot}
              width={"12px"}
              alt=""
              style={{ margin: "0 5px" }}
            />{" "}
            + K )
          </div>
        </Popover>

        <div className="right-tools">
          <img src={message} alt="information" width={"19px"} />

          <div style={{width:'20px'}}></div>

          <Dropdown
            menu={{
              items,
            }}
          >
            <div className="avatar-dropdown">
              <Avatar
                size={20}
                style={{
                  backgroundColor: "#5cecc5",
                  color: "#fff",
                  fontSize:'15px'
                }}
              >
                T
              </Avatar>
              <DownOutlined
                style={{
                  color: "#fff",
                }}
              />
            </div>
          </Dropdown>
        </div>
      </Header>
    </>
  );
};

export default MyHeader;
