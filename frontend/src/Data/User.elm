module Data.User exposing
  ( User
  , decoder
  )

import Json.Decode as Decode exposing (Decoder)
import Json.Encode as Encode exposing (Value)

import Json.Decode.Pipeline as Pipeline exposing (decode, required)


type alias User =
  { username : String
  , email : String
  , fullName : String
  , about : Maybe String
  }


decoder : Decoder User
decoder =
  decode User
    |> required "username" Decode.string
    |> required "email" Decode.string
    |> required "full_name" Decode.string
    |> required "about" (Decode.nullable Decode.string)
