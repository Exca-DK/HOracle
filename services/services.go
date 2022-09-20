package services

import (
	"github.com/Exca-DK/HoudiniPrometheus/core"

	ParamUpdatedServiceSet "github.com/Exca-DK/HoudiniPrometheus/services/paramUpdated/endpoint"
	ParamUpdatedService "github.com/Exca-DK/HoudiniPrometheus/services/paramUpdated/service"

	NodeCreatedServiceSet "github.com/Exca-DK/HoudiniPrometheus/services/nodeCreated/endpoint"
	NodeCreatedService "github.com/Exca-DK/HoudiniPrometheus/services/nodeCreated/service"

	NodeDeletedServiceSet "github.com/Exca-DK/HoudiniPrometheus/services/nodeDeleted/endpoint"
	NodeDeletedService "github.com/Exca-DK/HoudiniPrometheus/services/nodeDeleted/service"

	renderActivityServiceSet "github.com/Exca-DK/HoudiniPrometheus/services/renderActivity/endpoint"
	renderActivityService "github.com/Exca-DK/HoudiniPrometheus/services/renderActivity/service"

	sceneSavedServiceSet "github.com/Exca-DK/HoudiniPrometheus/services/sceneSaved/endpoint"
	sceneSavedService "github.com/Exca-DK/HoudiniPrometheus/services/sceneSaved/service"

	viewportActivityServiceSet "github.com/Exca-DK/HoudiniPrometheus/services/viewportActivity/endpoint"
	viewportActivitService "github.com/Exca-DK/HoudiniPrometheus/services/viewportActivity/service"
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
