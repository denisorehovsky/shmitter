module Test.Data exposing (..)

import Json.Decode as Decode
import Json.Encode as Encode

import Expect
import Test exposing (..)

import Data.Token as Token exposing (Token)
import Data.User as User exposing (User)


tokenTests : Test
tokenTests =
  describe "Token"
    [ test "Properly decodes a token" <|
      \() ->
        "\"4n-50689d23\""
          |> Decode.decodeString Token.decoder
          |> Expect.equal ( Ok (Token.Token "4n-50689d23") )
    , test "Properly encodes a token" <|
      \() ->
        Token.Token "4n-50689d23"
          |> Token.encode
          |> Encode.encode 0
          |> Expect.equal "\"4n-50689d23\""
    , test "Properly decodes from json" <|
      \() ->
        Encode.string "\"4n-50689d23\""
          |> Token.decodeTokenFromJson
          |> Maybe.withDefault (Token.Token "")
          |> Expect.equal (Token.Token "4n-50689d23")
    ]


userTests : Test
userTests =
  describe "User"
  [ test "Properly decodes a user" <|
    \() ->
      let
        json =
          """
          {
            "username": "testuser",
            "email": "testuser@shmitter.com",
            "full_name": "Test User",
            "about": null
          }
          """
        expectedUser =
          User.User
            "testuser"
            "testuser@shmitter.com"
            "Test User"
            Nothing
      in
        json
          |> Decode.decodeString User.decoder
          |> Expect.equal ( Ok expectedUser )
  ]
