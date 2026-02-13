import { LayoutDashboard, Thermometer, SprayCan, Bubbles } from 'lucide-react';
import { DynamicIcon } from 'lucide-react/dynamic';

function Icon({ name, size }) {
    const lucideMapper = {
        "layout-dashboard": <LayoutDashboard color='black' size={size} />,
        "bubbles": <Bubbles color='black' size={size} />,
        "spray-can": <SprayCan color='black' size={size} />,
        "thermometer": <Thermometer color='black' size={size} />,
    }

    return (
        <>
            {lucideMapper[name]}
        </>
    )

}

export { Icon };