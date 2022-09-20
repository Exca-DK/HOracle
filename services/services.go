package services

import (
	"github.com/Exca-DK/HOracle/core"

	ParamUpdatedServiceSet "github.com/Exca-DK/HOracle/services/paramUpdated/endpoint"
	ParamUpdatedService "github.com/Exca-DK/HOracle/services/paramUpdated/service"

	NodeCreatedServiceSet "github.com/Exca-DK/HOracle/services/nodeCreated/endpoint"
	NodeCreatedService "github.com/Exca-DK/HOracle/services/nodeCreated/service"

	NodeDeletedServiceSet "github.com/Exca-DK/HOracle/services/nodeDeleted/endpoint"
	NodeDeletedService "github.com/Exca-DK/HOracle/services/nodeDeleted/service"

	renderActivityServiceSet "github.com/Exca-DK/HOracle/services/renderActivity/endpoint"
	renderActivityService "github.com/Exca-DK/HOracle/services/renderActivity/service"

	sceneSavedServiceSet "github.com/Exca-DK/HOracle/services/sceneSaved/endpoint"
	sceneSavedService "github.com/Exca-DK/HOracle/services/sceneSaved/service"

	viewportActivityServiceSet "github.com/Exca-DK/HOracle/services/viewportActivity/endpoint"
	viewportActivitService "github.com/Exca-DK/HOracle/services/viewportActivity/service"
)

type ServiceBundle struct {
	Service core.Service
	Set     core.IESet
}

func GetAllServices() []ServiceBundle {
	paramBundle := ServiceBundle{
		Service: ParamUpdatedService.NewService(),
		Set:     ParamUpdatedServiceSet.NewEndpointSet(),
	}
	nodeCreatedBundle := ServiceBundle{
		Service: NodeCreatedService.NewService(),
		Set:     NodeCreatedServiceSet.NewEndpointSet(),
	}
	nodeDeletedBundle := ServiceBundle{
		Service: NodeDeletedService.NewService(),
		Set:     NodeDeletedServiceSet.NewEndpointSet(),
	}
	renderActivityBundle := ServiceBundle{
		Service: renderActivityService.NewService(),
		Set:     renderActivityServiceSet.NewEndpointSet(),
	}
	sceneSavedBundle := ServiceBundle{
		Service: sceneSavedService.NewService(),
		Set:     sceneSavedServiceSet.NewEndpointSet(),
	}
	viewportActivityBundle := ServiceBundle{
		Service: viewportActivitService.NewService(),
		Set:     viewportActivityServiceSet.NewEndpointSet(),
	}
	return []ServiceBundle{paramBundle, nodeCreatedBundle, nodeDeletedBundle, renderActivityBundle, sceneSavedBundle, viewportActivityBundle}
}
