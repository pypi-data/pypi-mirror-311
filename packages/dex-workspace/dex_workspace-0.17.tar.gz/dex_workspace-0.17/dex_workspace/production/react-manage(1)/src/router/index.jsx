import { Navigate } from "react-router-dom";
// const My = lazy(()=>import('@/views/My')); //路由懒加载

import Page1 from "@/pages/page1";
import Page2 from "@/pages/page2";
import Page3 from "@/pages/page3";
import Page4 from "@/pages/page4";
import Page5 from "@/pages/page5";
import Page11 from "@/pages/page11";
import Page12 from "@/pages/page12";
import Page5_1 from "../pages/page5_1";
import Password_PAGE from "../pages/password/password";

const router = [
  {
    path: "/",
    name: "Page1",
    element: <Page1 />,
  },
  {
    path: "/page-1",
    name: "Page1",
    element: <Page1 />,
  },
  {
    path: "/page-2",
    name: "Page2",
    element: <Page2 />,
  },
  {
    path: "/page-3",
    name: "Page3",
    element: <Page3 />,
  },
  {
    path: "/page-4",
    name: "Page4",
    element: <Page4 />,
  },
  {
    path: "/page-5",
    name: "Page5",
    element: <Page5_1 />,
  },
  {
    path: "/page-11",
    name: "Page11",
    element: <Page11 />,
  },
  //   配置路由重定向 可配置404页面
  {
    path: "*",
    element: <Navigate to="/" />,
  },
];

export default router;
