# -*- encoding: utf-8 -*-

import time
import platform
import json

# https://pyobjc.readthedocs.io/en/latest/notes/framework-wrappers.html
import objc
import CoreWLAN

from . import yy_wifi_helper

# https://github.com/ronaldoussoren/pyobjc/tree/master/pyobjc-framework-CoreWLAN
# https://developer.apple.com/documentation/corewlan/cweventdelegate?language=objc
# https://github.com/ronaldoussoren/pyobjc/blob/master/pyobjc-framework-CoreWLAN/PyObjCTest/test_cwwificlient.py
# CoreWLAN.CWEventDelegate

# https://developer.apple.com/documentation/corewlan/cweventdelegate/1512395-linkdidchangeforwifiinterfacewit?language=objc
class YYMacOSCoreWLANHelper(CoreWLAN.NSObject):
    def __init__(self):
        print("in YYMacOSCoreWLANHelper init")
        self.eventHelper = None

    def setCallback_(self, handler, debug:bool = False):
        if handler != None and hasattr(handler, 'eventCallback'):
            self.eventHelper = handler
        self.eventHelperDebug = debug

    def removeCallback(self):
        self.eventHelper = None

    def bssidDidChangeForWiFiInterfaceWithName_(self, interfaceName):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print(f"bssidDidChangeForWiFiInterfaceWithName: {interfaceName}")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': f"bssidDidChangeForWiFiInterfaceWithName: {interfaceName}",
            })

    def clientConnectionInterrupted(self):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print("clientConnectionInterrupted")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': 'clientConnectionInterrupted',
            })

    def clientConnectionInvalidated(self):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print("clientConnectionInvalidated")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': 'clientConnectionInvalidated',
            })

    def countryCodeDidChangeForWiFiInterfaceWithName_(self, interfaceName):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print(f"countryCodeDidChangeForWiFiInterfaceWithName: {interfaceName}")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': f"countryCodeDidChangeForWiFiInterfaceWithName: {interfaceName}",
            })

    def linkDidChangeForWiFiInterfaceWithName_(self, interfaceName):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print(f"linkDidChangeForWiFiInterfaceWithName: {interfaceName}")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': f"linkDidChangeForWiFiInterfaceWithName: {interfaceName}",
            })

    def modeDidChangeForWiFiInterfaceWithName_(self, interfaceName):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print(f"modeDidChangeForWiFiInterfaceWithName: {interfaceName}")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': f"modeDidChangeForWiFiInterfaceWithName: {interfaceName}",
            })

    def linkQualityDidChangeForWiFiInterfaceWithName_rssi_transmitRate_(self, nm, rs, tr):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print("linkQualityDidChangeForWiFiInterfaceWithName_rssi_transmitRate_")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': f"linkQualityDidChangeForWiFiInterfaceWithName: {nm}, rssi: {rs}, rate: {tr}",
            })

    def powerStateDidChangeForWiFiInterfaceWithName_(self, interfaceName):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print(f"powerStateDidChangeForWiFiInterfaceWithName: {interfaceName}")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': f"powerStateDidChangeForWiFiInterfaceWithName: {interfaceName}",
            })

    def ssidDidChangeForWiFiInterfaceWithName_(self, interfaceName):
        if hasattr(self, 'eventHelperDebug') and self.eventHelperDebug:
            print(f"ssidDidChangeForWiFiInterfaceWithName: {interfaceName}")
        if hasattr(self, 'eventHelper') and self.eventHelper != None and callable(self.eventHelper.eventCallback):
            self.eventHelper.eventCallback({
                'raw': f"ssidDidChangeForWiFiInterfaceWithName: {interfaceName}",
            })

class YYMacOSWIFIHelper(yy_wifi_helper.YYOSWIFIHelper):
    def __init__(self):
        self.client = CoreWLAN.CWWiFiClient.alloc().init()
        #print(CoreWLAN.CWWiFiClient.interfaceNames())
        self.systemEventHandler = None

    def __del__(self):
        self.disableEventHandler()
        del self.client
        self.client = None
        if self.systemEventHandler != None:
            self.systemEventHandler.removeCallback()
        self.systemEventHandler = None

    def disableEventHandler(self):
        if self.systemEventHandler == None:
            return
        success = self.client.stopMonitoringAllEventsAndReturnError_(None)
        if success:
            print("self.client.stopMonitoringAllEventsAndReturnError_ success")
        else:
            print("self.client.stopMonitoringAllEventsAndReturnError_ error")
        self.client.setDelegate_(None)

    def enableEventHandler(self, handler:yy_wifi_helper.YYWIFIHelper, debug:bool = False ):
        if self.systemEventHandler == None:
            self.systemEventHandler = YYMacOSCoreWLANHelper.alloc().init()
            if handler != None:
                self.systemEventHandler.setCallback_(handler, debug)
        
            # https://developer.apple.com/documentation/corewlan/cweventtype?language=objc
            self.client.setDelegate_(self.systemEventHandler)
            for option in [
                    CoreWLAN.CWEventTypeSSIDDidChange,
                    CoreWLAN.CWEventTypeLinkDidChange,
                    CoreWLAN.CWEventTypeLinkQualityDidChange,
                    CoreWLAN.CWEventTypeScanCacheUpdated,
                    CoreWLAN.CWEventTypeCountryCodeDidChange,
                    CoreWLAN.CWEventTypeBSSIDDidChange,
                    #CoreWLAN.CWEventTypeScanCacheUpdated,
                    #CoreWLAN.CWEventTypeUnknown,
                    #CoreWLAN.CWEventTypeNone,
            ]:
                success = self.client.startMonitoringEventWithType_error_(option, None)
                if success:
                    if debug:
                        print(f"self.client.startMonitoringEventWithType_error_ success: {option}")
    
    def getConnectedAPSSID(self, targetInterface: str | None = None) -> (bool, str | None, str | None):
        output = None
        try:
            currentInterface = self.getInterface()
            if targetInterface is None:
                targetInterface = currentInterface['default']
            elif targetInterface not in currentInterface['list']:
                return (False, output, f"interface not found: {targetInterface}")
        except Exception as e:
            return (False, output, f"find interface error: {targetInterface}, {str(e)}")

        targetRealInterface = None
        try:
            # https://developer.apple.com/documentation/corewlan/cwwificlient/1512328-interface
            targetRealInterface = self.client.interfaceWithName_(targetInterface)
        except Exception as e:
            targetRealInterface = None
            return (False, output, f"client.interface(withName): {str(e)}")

        if targetRealInterface == None:
            return (False, output, f"interface is empty")

        try:
            currentNetworkSSID = targetRealInterface.ssid()
            output = currentNetworkSSID
        except Exception as e:
            return (False, output, f"get ssid error: {str(e)}")

        return (True, output)

    def disconnect(self, targetInterface:str | None = None, asyncMode: bool = False, asyncWaitTimeout: int = 15) -> (bool, str):
        try:
            currentInterface = self.getInterface()
            if targetInterface is None:
                targetInterface = currentInterface['default']
            elif targetInterface not in currentInterface['list']:
                return (False, f"interface not found: {targetInterface}")
        except Exception as e:
            return (False, f"find interface error: {targetInterface}, {str(e)}")

        targetRealInterface = None
        try:
            # https://developer.apple.com/documentation/corewlan/cwwificlient/1512328-interface
            targetRealInterface = self.client.interfaceWithName_(targetInterface)
        except Exception as e:
            targetRealInterface = None
            return (False, f"client.interface(withName): {str(e)}")

        if targetRealInterface == None:
            return (False, f"interface is empty")

        try:
            targetRealInterface.disassociate()
        except Exception as e:
            return (False, f"disassociate error: {str(e)}")

        if asyncMode == False:
                waitCount = asyncWaitTimeout + 0.5
                currentConnectedSSID = None
                while waitCount > 0.5:
                    queryStatus, currentConnectedSSID = self.getConnectedAPSSID(targetInterface)
                    if queryStatus and currentConnectedSSID == None:
                        break
                    time.sleep(0.1)
                    waitCount -= 0.1
                if currentConnectedSSID != None:
                    return (False, 'disassociate timeout')

        return (True, None)

    def connectToAP(self, targetSSID:str , targetPassword: str | None = None, targetSecurity: yy_wifi_helper.YYWIFISecurityMode | None = None, findSSIDBeforeConnect:bool = False, targetInterface: str | None = None, asyncMode: bool = False, asyncWaitTimeout: int = 15) -> (bool, str):
        timeCost = {
            'total': 0.0,
            'scan': 0.0,
            'connect': 0.0,
            'connected': 0.0,
        }
        timeCost['total'] = time.time()
        try:
            currentInterface = self.getInterface()
            if targetInterface is None:
                targetInterface = currentInterface['default']
            elif targetInterface not in currentInterface['list']:
                return (False, f"interface not found: {targetInterface}")
        except Exception as e:
            return (False, f"find interface error: {targetInterface}, {str(e)}")

        targetRealInterface = None
        try:
            # https://developer.apple.com/documentation/corewlan/cwwificlient/1512328-interface
            targetRealInterface = self.client.interfaceWithName_(targetInterface)
        except Exception as e:
            targetRealInterface = None
            return (False, f"client.interface(withName): {str(e)}")

        if targetRealInterface == None:
            return (False, f"interface is empty")

        queryCurrentConnectedSSID, queryLog = self.getConnectedAPSSID(targetInterface)
        if queryCurrentConnectedSSID == False:
            return (False, f"getConnectedAP error: {queryLog}")
        if queryLog != None:
            if queryLog == targetSSID:
                return (True, f"errorMessage: Already connected to the specified SSID")

        result = False
        errorMessage = None
        if findSSIDBeforeConnect:
            timeCost['scan'] = time.time()
            # https://developer.apple.com/documentation/corewlan/cwinterface/1426436-scanfornetworkswithssid?language=objc
            errorLog = None
            networks, error = targetRealInterface.scanForNetworksWithSSID_error_(targetSSID.encode("utf-8"), errorLog)
            timeCost['scan'] = time.time() - timeCost['scan']
            if error:
                return (False, f"targetRealInterface.scanForNetworksWithName_error_: {targetSSID}, error: {str(error)}, errorLog: {str(errorLog)}")
            if len(networks) == 0:
                return (False, f"targetRealInterface.scanForNetworksWithName_error_: no networks (find '{targetSSID}')")

            targetNetwork = None
            for n in networks:
                targetNetwork = n

            if targetNetwork == None:
                return (False, f"targetNetwork is empty")

            timeCost['connect'] = time.time()
            try:
                # https://developer.apple.com/documentation/corewlan/cwinterface/1426455-associatetonetwork?language=objc
                success = targetRealInterface.associateToNetwork_password_error_(targetNetwork, targetPassword, errorLog)
                if success:
                    result = True
                else:
                    errorMessage = f"connect error with log: {str(errorLog)}"
            except Exception as e:
                result = False

            timeCost['connect'] = time.time() - timeCost['connect']
        else:
            return (False, 'TODO - macOS Not Support( findSSIDBeforeConnect = False )')
            networkProfile = CoreWLAN.CWMutableNetworkProfile.alloc().init()
            networkProfile.setSsidData_(targetSSID.encode('utf-8'))
            if targetPassword != None:
                # https://developer.apple.com/documentation/corewlan/cwsecurity?language=objc
                networkProfile.setSecurity_(CoreWLAN.kCWSecurityWPA2Personal)
            #config.phrase = targetPassword

            networkConfig = CoreWLAN.CWMutableConfiguration.alloc().init()
            networkConfig.setNetworkProfiles_([networkProfile])

            success: Unknown = targetRealInterface.commitConfiguration_authorization_error_(networkConfig, None, objc.NULL)
            #if success:
            #    print("Done Sucess")

        if result:
            if asyncMode == False:
                timeCost['connected'] = time.time()
                waitCount = asyncWaitTimeout + 0.5
                currentConnectedSSID = None
                while waitCount > 0.5:
                    queryStatus, queryLog = self.getConnectedAPSSID(targetInterface)
                    if queryStatus and queryLog != None and queryLog == targetSSID:
                        currentConnectedSSID = queryLog
                        break
                    time.sleep(0.1)
                    waitCount -= 0.1
                result = currentConnectedSSID == targetSSID
                timeCost['connected'] = time.time() - timeCost['connected']

        timeCost['total'] = time.time() - timeCost['total']
        errorMessage = f"time cost: {timeCost}" if errorMessage == None else f"{errorMessage}, time cost: {timeCost}"
        return (result, errorMessage)

    def scanToGetAPList(self, targetInterface:str | None = None):
        output = { 'status': False, 'list': [] , 'error': None }
        target = None
        try:
            currentInterface = self.getInterface()
            if targetInterface is None:
                targetInterface = currentInterface['default']
            elif targetInterface not in currentInterface['list']:
                errorMessage = f"interface not found: {targetInterface}, current: {currentInterface['list']}"
                output['error'] = [errorMessage]
                return output
        except Exception as e:
            errorMessage = f"interface error: {targetInterface}"
            if output['error'] is None:
                output['error'] = [errorMessage]
            else:
                output['error'].append(errorMessage) 
            return output

        try:
            # https://developer.apple.com/documentation/corewlan/cwwificlient/1512328-interface
            target = self.client.interfaceWithName_(targetInterface)
        except Exception as e:
            target = None
            errorMessage = f"client.interface(withName): {str(e)}"
            if output['error'] is None:
                output['error'] = [errorMessage]
            else:
                output['error'].append(errorMessage) 

        if target == None:
            return output

        try:
            ssid, err = target.scanForNetworksWithName_error_(None, None)
            if err == None:
                output['status'] = True
                for item in ssid:
                    try:
                        itemOutput = {
                            yy_wifi_helper.WIFIAP.SSID: item.ssid(),
                            yy_wifi_helper.WIFIAP.BSSID: item.bssid(),
                            yy_wifi_helper.WIFIAP.RSSI: item.rssiValue(),
                            yy_wifi_helper.WIFIAP.IBSS: item.ibss(),
                            yy_wifi_helper.WIFIAP.SECURITY: None,
                            yy_wifi_helper.WIFIAP.CHANNEL_BAND: None,
                            yy_wifi_helper.WIFIAP.CHANNEL_NUMBER: None,
                            yy_wifi_helper.WIFIAP.CHANNEL_WIDTH: None,
                        }

                        try:
                            itemOutput[yy_wifi_helper.WIFIAP.SECURITY] = item.security()
                        except Exception as e:
                            errorMessage = f"item.security(): {str(e)}"
                            if output['error'] is None:
                                output['error'] = [errorMessage]
                            else:
                                output['error'].append(errorMessage) 

                        try:
                            itemOutput[yy_wifi_helper.WIFIAP.CHANNEL_BAND] = item.wlanChannel().channelBand()
                            itemOutput[yy_wifi_helper.WIFIAP.CHANNEL_NUMBER] = item.wlanChannel().channelNumber()
                            itemOutput[yy_wifi_helper.WIFIAP.CHANNEL_WIDTH] = item.wlanChannel().channelWidth()
                        except Exception as e:
                            errorMessage = f"item.wlanChannel()->channelBand(),channelNumber(),channelWidth(): {str(e)}"
                            if output['error'] is None:
                                output['error'] = [errorMessage]
                            else:
                                output['error'].append(errorMessage) 

                        itemOutput['object'] = item
                        output['list'].append(itemOutput)
                    except Exception as e:
                        errorMessage = f"item->ssid(), bssid(), rssiValue(), ibss(): {str(e)}"
                        if output['error'] is None:
                            output['error'] = [errorMessage]
                        else:
                            output['error'].append(errorMessage) 
            else:
                errorMessage = f"scanForNetworksWithName_error_: {str(err)}"
                if output['error'] is None:
                    output['error'] = [errorMessage]
                else:
                    output['error'].append(errorMessage) 
        except Exception as e:
            errorMessage = f"item->ssid(), bssid(), rssiValue(), ibss(): {str(e)}"
            if output['error'] is None:
                output['error'] = [errorMessage]
            else:
                output['error'].append(errorMessage) 

        return output

    def getInterface(self):
        output = { 'default': None, 'list': [], 'error': None }

        # https://developer.apple.com/documentation/corewlan/cwwificlient
        try:
            output['default'] = self.client.interface().interfaceName()
        except Exception as e:
            output['error'] = [e] if output['error'] is None else output['error'].append(e)

        try:
            for item in self.client.interfaces():
                try:
                    output['list'].append(item.interfaceName())
                except Exception as e:
                    output['error'] = [e] if output['error'] is None else output['error'].append(e)
        except Exception as e:
            output['error'] = [e] if output['error'] is None else output['error'].append(e)
        
        return output

    def scanToGetAPListInJSON(self, targetInterface: str | None = None):
        output = self.scanToGetAPList(targetInterface)
        if output['status'] == True:
            for i in range(len(output['list'])):
                del output['list'][i]['object']
        try:
            return json.dumps(output, indent=4)
        except Exception as e:
            return {'error': str(e)}
