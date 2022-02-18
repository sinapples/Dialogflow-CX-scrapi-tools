from dfcx_scrapi.core.intents import Intents
from dfcx_scrapi.core.flows import Flows
from dfcx_scrapi.core.pages import Pages
from dfcx_scrapi.tools.maker_util import MakerUtil
 
 

def __main__():
    creds_path = 'creds.json'
    agentID = "projects/ID/locations/ID/agents/ID" 
    targetPage = "projects/ID/locations/ID/agents/ID/flows/ID/pages/ID"
    addAllIntentsToDefaultStart(creds_path,agentID,targetPage)


# Input agentID and a targent page ID 
# Results in all intents in the agents will be added to the Start Page of the Default Start Flow with a transition route to targetPage
def addAllIntentsToDefaultStart( creds_path,agentID, targetPage ):
   
    # First, we will instantiate our Flows and Pages objects.
    f = Flows(creds_path=creds_path)
    p = Pages(creds_path=creds_path)
    mu = MakerUtil()


    flows_map = f.get_flows_map(agentID, reverse=True)

    # Get Default Start Flow
    dsf = f.get_flow(flows_map['Default Start Flow'])


    # Get all intents in the Agent
    i = Intents(creds_path=creds_path)
    intent_list = i.list_intents(agentID)

 
    # Create all routes using Maker Util
    for intent in intent_list:

        # Ignore default intents
        if "Default Welcome Intent" in intent.display_name or "Default Negative Intent" in intent.display_name:
            continue
        
        #Prints progress 
        print(intent.display_name, end=" ")

        # Create Route
        my_tr = mu.make_transition_route(
            intent=intent.name, target_page=targetPage)
        dsf.transition_routes.append(my_tr)

    # Update the flow with the new routes
    f.update_flow(
        flows_map['Default Start Flow'],
        obj=dsf,
        transition_routes=dsf.transition_routes)
    print()


__main__()