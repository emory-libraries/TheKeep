require 'rubygems'
require 'json'
require 'pry'
require 'csv'

# This is a Ruby script that parses csvdiff outputs
# and generates corresponding CSV files.
# TODO: There will be a more in-depth instruction included shortly.
# For now this is a placeholder to have the script committed and published.

# Requires the input JSON named as `diff.json`
file = File.read('diff.json')
data_hash = JSON.parse(file)

# Handle changed objects
CSV.open('changed.csv','wb') do |csvfile|
  csvfile << ["changed", "pid", "from_label", "to_label", "from_path", "to_path"]
  data_hash['changed'].each do |row|
    array = ["changed"]

    if defined? row["key"]
      array = array + row["key"]
    end

    if defined? row["fields"]["LABEL"]["from"]
      array = array + [row["fields"]["LABEL"]["from"]]
      array = array + [row["fields"]["LABEL"]["to"]]
    else
      array = array + ["NOT_CHANGED"]
      array = array + ["NOT_CHANGED"]
    end

    if defined? row["fields"]["PATH"]["from"]
      array = array + [row["fields"]["PATH"]["from"]]
      array = array + [row["fields"]["PATH"]["to"]]
    else
      array = array + ["NOT_CHANGED"]
      array = array + ["NOT_CHANGED"]
    end

    csvfile << array

  end
end

# Handle added objects
CSV.open('added.csv','wb') do |csvfile|
  csvfile << ["added", "pid", "label", "path"]
  data_hash['added'].each do |row|
    csvfile << ["added", row["PID"], row["LABEL"], row["PATH"]]
  end
end

# Handle removed objects
CSV.open('removed.csv','wb') do |csvfile|
  csvfile << ["removed", "pid", "label", "path"]
  pry
  data_hash['removed'].each do |row|
    csvfile << ["removed", row["PID"], row["LABEL"], row["PATH"]]
  end
end
