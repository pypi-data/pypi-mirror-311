import "./style.scss";
import React, { useEffect, useState } from "react";
import { CheckOutlined } from "@ant-design/icons";
import { Input, ConfigProvider, Popover } from "antd";
import EditSvg from "@/assets/svg/edit.svg";
import WordSvg from "@/assets/svg/word.svg";

// Moved RowPopoverContent outside of RowPopover to optimize rendering
const RowPopoverContent = React.memo(({
  isEdit,
  isOnlyShow,
  showText,
  popoverEditText,
  onTextChange,
  onSave,
  toggleEdit
}) => {
  return (
    <div className="my-popover-content">
      <div className="my-popover-content-header">
        <div className="flex-center-xy">
          <img src={WordSvg} alt="Text" width={30} />
          <span className="my-popover-content-header-text">TEXT</span>
        </div>
        {!isOnlyShow &&
          (isEdit ? (
            <CheckOutlined
              style={{ color: "#57a2ff", fontSize: 18 }}
              onClick={onSave}
            />
          ) : (
            <img
              src={EditSvg}
              alt="edit"
              style={{ cursor: "pointer" }}
              onClick={toggleEdit}
            />
          ))}
      </div>
      <div>
        {isEdit ? (
          <Input.TextArea
            value={popoverEditText}
            autoSize={{ minRows: 10, maxRows: 10 }}
            onChange={(e) => onTextChange(e.target.value)}
          />
        ) : (
          <div>{isOnlyShow ? showText : popoverEditText}</div>
        )}
      </div>
    </div>
  );
});

const RowPopover = ({
  showText,
  item,
  index,
  isOnlyShow,
  saveCallback,
  children,
}) => {
  const [isEdit, setIsEdit] = useState(false);
  const [popoverEditText, setPopoverEditText] = useState("");

  useEffect(() => {
    if (typeof showText === "string") {
      setPopoverEditText(showText);
    }
  }, [showText]);

  const saveEditPopoverContent = () => {
    if (typeof saveCallback === "function") {
      saveCallback(index, popoverEditText);
    }
    setIsEdit(false);
  };

  return (
    <ConfigProvider
      theme={{
        token: {
          sizePopupArrow: 0,
        },
      }}
    >
      <Popover
        id="my-row-popover"
        content={
          <RowPopoverContent
            isEdit={isEdit}
            isOnlyShow={isOnlyShow}
            showText={showText}
            popoverEditText={popoverEditText}
            onTextChange={setPopoverEditText}
            onSave={saveEditPopoverContent}
            toggleEdit={() => setIsEdit(true)}
          />
        }
        placement="bottomRight"
        trigger="click"
        onOpenChange={() => setIsEdit(false)}
      >
        {children}
      </Popover>
    </ConfigProvider>
  );
};

export default RowPopover;
