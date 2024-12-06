//
// Created by marcel on 26.05.21.
//

#ifndef FICTION_NETWORK_WRITER_HPP
#define FICTION_NETWORK_WRITER_HPP

#include "fiction/io/dot_drawers.hpp"

#include <mockturtle/io/write_dot.hpp>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

namespace fiction::debug
{

template <typename Ntk, typename Drawer = fiction::technology_dot_drawer<Ntk, true>>
void write_dot_network(const Ntk& ntk, const std::string& name = "ntk", const std::filesystem::path& p = {"./"})
{
    std::ofstream file{p / (name + ".dot")};

    mockturtle::write_dot(ntk, file, Drawer{});

    file.close();
}

template <typename Lyt, typename Drawer = fiction::gate_layout_cartesian_drawer<Lyt, false, true>>
void write_dot_layout(const Lyt& lyt, const std::string& name = "lyt", const std::filesystem::path& p = {"./"})
{
    std::ofstream file{p / (name + ".dot")};

    fiction::write_dot_layout(lyt, file, Drawer{});

    file.close();
}

}  // namespace fiction::debug

#endif  // FICTION_NETWORK_WRITER_HPP
