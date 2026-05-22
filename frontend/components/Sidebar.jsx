import "../scss/components/sidebar.scss";
import raspi from "../assets/raspi.svg";
import { Button } from "./Button";
import { PATHS } from "../globals";
import { viteUrl } from "../utils/vite-url";
import { GraphInterface } from "./GraphInterface";

const logoUrl = viteUrl(raspi);

function Sidebar({ setGraph }) {
  return (
    <aside className="dash-sidebar dash-container">
      <img src={logoUrl} className="dash-sidebar_logo" />
      <GraphInterface setGraph={setGraph} />
      <Button
        className="btn-sidebar"
        target={PATHS.RECORDINGS}
        setGraph={setGraph}
        text="Security Recordings"
        icon="camera"
      />
    </aside>
  );
}

export { Sidebar };
