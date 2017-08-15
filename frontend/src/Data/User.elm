module Data.User exposing
  ( User
  , decoder
  , Username(..)
  , usernameToString
  , usernameDecoder
  , usernameEncode
  )

import Json.Decode as Decode exposing (Decoder)
import Json.Encode as Encode exposing (Value)

import Json.Decode.Pipeline as Pipeline exposing (decode, required)


type alias User =
  { username : Username
  , email : String
  , fullName : String
  , about : Maybe String
  }


decoder : Decoder User
decoder =
  decode User
    |> required "username" usernameDecoder
    |> required "email" Decode.string
    |> required "full_name" Decode.string
    |> required "about" (Decode.nullable Decode.string)



-- IDENTIFIERS


type Username
  = Username String


usernameToString : Username -> String
usernameToString (Username username) =
  username


usernameDecoder : Decoder Username
usernameDecoder =
  Decode.map Username Decode.string


usernameEncode : Username -> Value
usernameEncode (Username username) =
  Encode.string username
