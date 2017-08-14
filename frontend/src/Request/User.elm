module Request.User exposing (fetchByToken)

import Http
import HttpBuilder

import Data.Token exposing (Token)
import Data.User as User exposing (User)
import Request.Helpers exposing (apiUrl)
import Request.Token


fetchByToken : Token -> Http.Request User
fetchByToken token =
  apiUrl "/users/me/"
    |> HttpBuilder.get
    |> HttpBuilder.withExpect (Http.expectJson User.decoder)
    |> Request.Token.withAuthorization (Just token)
    |> HttpBuilder.toRequest
