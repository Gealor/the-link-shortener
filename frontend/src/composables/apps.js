import { markRaw } from 'vue'
import explorerIcon from '../assets/icons/msie1-5.png'
import htmlIcon from '../assets/icons/html-1.png'
import computerIcon from '../assets/icons/computer_2-2.png'
import ExplorerApp from '../components/ExplorerApp.vue'
import TestApp from '../components/MyComputer.vue'

export const appsRegistry = {
  internetExplorer: {
    id: 'internetExplorer',
    title: 'Internet Explorer',
    windowTitle: "Shortify - Microsoft Internet Explorer",
    icon: explorerIcon,
    windowIcon: htmlIcon,
    component: markRaw(ExplorerApp),
    quickLaunch: true,
    height: 400,
    width: 550,
  },
  myComputer: {
    id: 'myComputer',
    title: 'My Computer',
    windowTitle: "My Computer",
    icon: computerIcon,
    windowIcon: computerIcon,
    component: markRaw(TestApp),
    quickLaunch: true,
    height: 400,
    width: 600,
  },
}

export const quickLaunchApps = Object.values(appsRegistry).filter(a => a.quickLaunch)