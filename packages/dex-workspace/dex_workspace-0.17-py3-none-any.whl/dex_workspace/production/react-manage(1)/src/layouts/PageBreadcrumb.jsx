import { Breadcrumb, Avatar, Space } from "antd";

export default function PageBreadcrumb() {
  const items = [{ title: "Home", path: "/" }, { title: "Page" }];

  return (
    <>
      <div className="layout-breadcrumb">
        <Space>
          <Avatar
            size={26}
            shape="square"
            style={{
              backgroundColor: "#ef863d",
              color: "#fff",
            }}
          >
            T
          </Avatar>

        Testing version
        </Space>
      </div>
      <hr />
    </>
  );
}
