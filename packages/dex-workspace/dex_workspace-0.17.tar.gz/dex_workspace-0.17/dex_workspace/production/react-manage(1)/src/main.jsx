import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.scss";
import MyLayout from "@/layouts";
import { BrowserRouter } from "react-router-dom";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <MyLayout></MyLayout>
    </BrowserRouter>
  </StrictMode>
);
