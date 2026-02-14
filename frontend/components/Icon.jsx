import { LayoutDashboard, Thermometer, SprayCan, Bubbles, CircleGauge, RefreshCcw } from 'lucide-react';
import { DynamicIcon } from 'lucide-react/dynamic';

function Icon({ name, color, size }) {
    const lucideMapper = {
        "layout-dashboard": <LayoutDashboard color={color} size={size} />,
        "bubbles": <Bubbles color={color} size={size} />,
        "spray-can": <SprayCan color={color} size={size} />,
        "thermometer": <Thermometer color={color} size={size} />,
        "circle-gauge": <CircleGauge color={color} size={size} />,
        "refresh-cw": <RefreshCcw color={color} size={size} />,
    }

    return (
        <>
            {lucideMapper[name]}
        </>
    )

}

export { Icon };