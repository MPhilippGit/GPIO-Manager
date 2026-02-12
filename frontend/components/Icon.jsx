import { DynamicIcon } from 'lucide-react/dynamic';

function Icon({ name, size }) {
    return <DynamicIcon name={name} color='black' size={size} />
}

export { Icon };