from coveopush import CoveoPush
from coveopush import Document
from coveopush import CoveoPermissions
from coveopush import CoveoConstants

sourceId = 'pokemonchallengepebfwi56-tymrhcjeplqwiacezf4rr2cice'
orgId = 'pokemonchallengepebfwi56'
apiKey = 'xx0ff4f49e-ddda-45af-a9c0-0e7d899e06db'

push = CoveoPush.Push(sourceId, orgId, apiKey)
mydoc = Document("https://pokemondb.net/pokedex/national")
mydoc.Title = "THIS IS A TEST"
mydoc.SetData("ALL OF THESE WORDS ARE SEARCHABLE")
mydoc.FileExtension = ".html"
mydoc.AddMetadata("connectortype", "CSV")

user_email = "npushkarskii@coveo.com"
my_permissions = CoveoPermissions.PermissionIdentity(CoveoConstants.Constants.PermissionIdentityType.User, "", user_email)
allowAnonymous = True
mydoc.SetAllowedAndDeniedPermissions([my_permissions], [], allowAnonymous)

push.AddSingleDocument(mydoc)