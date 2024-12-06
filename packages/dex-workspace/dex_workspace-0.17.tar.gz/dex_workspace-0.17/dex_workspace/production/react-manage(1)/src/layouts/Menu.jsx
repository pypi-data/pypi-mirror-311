import { useEffect, useState } from "react";
import { PictureFilled } from "@ant-design/icons";
import { Layout } from "antd";
import { useNavigate, useLocation } from "react-router-dom";

import projects from '../assets/images/project.png'
import scripts from '../assets/images/scripts.png'
import data from '../assets/images/data.png'
import sharing from '../assets/images/nodes.png'
import shared from '../assets/images/shared.png'

import projects_color from '../assets/images/project-1.png'
import scripts_color from '../assets/images/scripts-1.png'
import data_color from '../assets/images/data-1.png'
import sharing_color from '../assets/images/nodes-1.png'
import shared_color from '../assets/images/shared-1.png'

const Menu = () => {
  const menuItems = [
    {
      path: "/page-1",
      icon: projects,
      label: "Home",
      alt: projects_color
    },
    {
      path: "/page-2",
      icon: scripts,
      label: "Scripts",
       alt: scripts_color,
    },
    {
      path: "/page-3",
      icon: data,
      label: "Data",
       alt: data_color,
    },
    {
      path: "/page-4",
      icon: sharing,
      label: "Sharing",
       alt: sharing_color
    },
    {
      path: "/page-5",
      icon: shared,
      label: "Shared",
       alt: shared_color
    },
  ];

  const [selectMenu, setSelectMenu] = useState(menuItems[0].path);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    setSelectMenu(
      location.pathname === "/" ? menuItems[0].path : location.pathname
    );
  }, [location]);

  const handleMenuItemClick = (item) => {
    navigate(item.path);
  };

  return (
    <>
      <Layout.Sider width={70} className="layout-sider">
        <ul className="layout-menu-ul">
          {menuItems.map((item) => (
            <li
              key={item.path}
              title={item.label}
              className={selectMenu === item.path ? "active" : ""}
              onClick={() => {
                handleMenuItemClick(item);
              }}
            >

              {/**/}
              <img src={selectMenu === item.path ? item.alt : item.icon} alt="" className='icon' />

              {/**/}

              <div style={{height:'5px'}}></div>
              <span className="text-line-1-ellipsis label">{item.label}</span>

            </li>
          ))}
        </ul>
      </Layout.Sider>
    </>
  );
};

              /**
              <p
                className="icon"
                style={{
                  color: selectMenu === item.path ? "#1890ff" : "#e7e9ed",
                }}
              >

                {selectMenu === item.path ? item.alt : item.icon}
              </p>

              */

export default Menu;
