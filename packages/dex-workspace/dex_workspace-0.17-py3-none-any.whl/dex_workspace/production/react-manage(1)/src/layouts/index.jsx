import { Layout } from "antd";
import { useRoutes, Routes, Route } from "react-router-dom";

import "./index.scss";
import MyMenu from "@/layouts/Menu.jsx";
import MyHeader from "@/layouts/Header.jsx";
import PageBreadcrumb from "@/layouts/PageBreadcrumb.jsx";
import routes from "@/router";

import Password_PAGE from "../pages/password/password"


const Platform = () => {
  const element = useRoutes(routes);

  return (
    <>
      <Layout className="my-layout">
        <MyHeader />
        <Layout className="layout">
          <MyMenu />
          <Layout className="layout-main">
            <PageBreadcrumb />

            <Layout.Content className="layout-content">
              {element}
            </Layout.Content>

            {/* 
            <Layout.Footer style={{ textAlign: "center" }}>
            </Layout.Footer>
            */}
          </Layout>
        </Layout>
      </Layout>
    </>
  );
}


const MyLayout = () => {
  const element = useRoutes(routes);

  return (
    <>

    <Routes>
      
      <Route path='*' element ={<Platform />} />

      <Route path='/login' element ={<Password_PAGE />} />

    </Routes>
    </>
  );
};



export default MyLayout;
