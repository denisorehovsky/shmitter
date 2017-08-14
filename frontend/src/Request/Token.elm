module Request.Token exposing
  ( obtain
  , withAuthorization
  )

import Json.Decode as Decode
import Json.Encode as Encode

import Http
import HttpBuilder exposing (RequestBuilder, withHeader)

import Data.Token as Token exposing (Token)
import Request.Helpers exposing (apiUrl)
import Utils exposing ((=>))


obtain : { r | usernameOrEmail : String, password : String } -> Http.Request Token
obtain { usernameOrEmail, password } =
  let
    body =
      Http.jsonBody <|
        Encode.object
          [ "username_or_email" => Encode.string usernameOrEmail
          , "password" => Encode.string password
          ]

    expect =
      Token.decoder
        |> Decode.field "token"
        |> Http.expectJson
  in
    apiUrl "/auth/token/obtain/"
      |> HttpBuilder.post
      |> HttpBuilder.withBody body
      |> HttpBuilder.withExpect expect
      |> HttpBuilder.toRequest


withAuthorization : Maybe Token -> RequestBuilder a -> RequestBuilder a
withAuthorization maybeToken builder =
  case maybeToken of
    Just token ->
      builder
        |> withHeader "Authorization" ( "JWT " ++ Token.tokenToString token )

    Nothing ->
      builder
