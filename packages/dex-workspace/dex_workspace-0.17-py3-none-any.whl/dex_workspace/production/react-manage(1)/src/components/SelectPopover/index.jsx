import "./style.scss";
import { Button, ConfigProvider, Avatar, Popover } from "antd";
import { PictureFilled } from "@ant-design/icons";

import { useState } from "react";

// Images
import code_file from "@/assets/images/document_code.png";

const PopoverContent = ({
  elements = [],
  onClose,
  complete, 
}) => {
  const [chooseValue, setChooseValue] = useState("");
  const [chooseItem, setChooseItem] = useState(null);

  const onClick = () => {
    onClose();
    if(chooseItem!==null){
      complete(chooseItem);
      setChooseItem(null);
    }
    setTimeout(() => {
      setChooseValue('');
    }, 1000);
  };

  return (
    <div className="my-custom-popover-content">
      <p className="my-custom-popover-content-label">Choose {chooseValue}</p>
      <ul>
        {elements.map((item, index) => (
          <li
            key={index}
            onClick={() => {
              setChooseValue(item.name);
              setChooseItem(item);
            }}
            className={chooseValue === item.name ? "active" : ""}
          >
            <Avatar size={25} shape="square" style={{backgroundColor:'transparent', padding:'0'}}>
              <img src={code_file} alt="" />
            </Avatar>
            <p className="text-line-1-ellipsis">{item.name}</p>
          </li>
        ))}
      </ul>
      <div className="flex-center-xy my-custom-popover-content-footer">
        <Button 
          block 
          type="primary" 
          disabled={!chooseValue}
          onClick={onClick}
        >
          Text
        </Button>
      </div>
    </div>
  );
};

const SelectPopover = ({ children, placement, elements=[], complete }) => {
  const [open, setOpen] = useState(false);

  return (
    <ConfigProvider
      theme={{
        token: {
          sizePopupArrow: 0,
        },
      }}
    >
      <Popover
        content={<PopoverContent elements={elements} onClose={() => setOpen(false)} complete={complete}/>}
        placement={placement ? placement : "leftTop"}
        id="my-custom-popover"
        trigger="click"
        open={open}
        onOpenChange={setOpen}
      >
        {children}
      </Popover>
    </ConfigProvider>
  );
};

export default SelectPopover;
